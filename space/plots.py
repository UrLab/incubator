from django_pandas.io import read_frame
import pandas as pd
import numpy as np
from .models import SpaceStatus, SpaceStatusPrediction
from django.utils import timezone

def get_openings_df(from_date, to_date, freq='H'):
    query = {}
    if from_date is not None:
        query['time__gte'] = from_date
    if to_date is not None:
        query['time__lt'] = to_date

    # Grab openings in a pandas dataframe
    df = read_frame(SpaceStatus.objects.filter(**query))
    start = pd.to_datetime(from_date).tz_localize('Europe/Brussels')
    end = pd.to_datetime(to_date).tz_localize('Europe/Brussels')

    # No records found, just return a fake df, always closed
    if len(df) == 0:
        df = pd.DataFrame([
            {'time': start, 'is_open': 0},
            {'time': end, 'is_open': 0}
        ])

    # Drop duplicate time index
    df = df.groupby(df.time).last()

    start = start.replace(minute=0, second=0, microsecond=0)
    end = end.replace(minute=0, second=0, microsecond=0)

    # Reindex on a monotonic time index
    index = pd.date_range(start=start, end=end, freq=freq)
    df = df.reindex(index, method='ffill')
    nans = np.isnan(df.is_open.astype(np.float64))
    df[nans] = not df[~nans].is_open[0]
    return df


def human_time(options):
    days_names = ["Lundi", "Mardi", "Mercredi",
                  "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    res = "Ouverture de UrLab: "
    if 'weeks' in options:
        res += "{} dernières semaines".format(options['weeks'])
    else:
        res += "{} - {}".format(options['from'], options['to'])
    if 'weekday' in options:
        res += " ({})".format(days_names[int(options['weekday'])])
    return res


def weekday_probs(opts):
    begin_hour = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_hour = begin_hour + timezone.timedelta(days=1)
    df = read_frame(SpaceStatusPrediction.objects.filter(time__gte=begin_hour, time__lt=end_hour))
    return df.proba_open
    # Create openings data query for requested time frame
    if 'weeks' in opts:
        delta = pd.Timedelta(days=7*int(opts['weeks']))
        now = pd.datetime.now()
        df = get_openings_df(now - delta, now)
    else:
        if 'from' in opts and 'to' in opts:
            df = get_openings_df(opts['from'], opts['to'], freq='H')

    if 'weekday_django' in opts:
        # Yes...  django: 0 == sunday; pandas: 0 == monday
        opts['weekday'] = (int(opts['weekday_django']) - 1) % 7
    if 'weekday' in opts:
        df = df[df.index.weekday == int(opts['weekday'])]

    # Group by hour and plot as image
    by_hour = df.groupby(df.index.time).is_open
    return by_hour.sum() / by_hour.count()


def weekday_plot(ax, opts):
    # Init plot
    width = int(opts.get('width', 12))
    height = int(opts.get('height', 8))
    ax.figure(figsize=(width, height))

    probs = 100 * weekday_probs(opts)
    img = np.repeat([probs], 5, axis=0)
    cax = ax.imshow(img, cmap=ax.cm.RdYlGn, interpolation='none',
                     vmin=0, vmax=100)
    ticks = [0, 25, 50, 75, 100]
    cbar = ax.colorbar(cax, ticks=ticks)
    cbar.ax.set_yticklabels(['{}%'.format(t) for t in ticks])

    # Ticks && grid
    ticks = np.arange(0, 24, 2)
    ax.xticks(ticks - 0.5, ["%dh" % x for x in ticks])
    ax.yticks([])
    ax.grid()

    # Title
    opts['from'] = df.index.min().strftime("%d/%m/%Y")
    opts['to'] = df.index.max().strftime("%d/%m/%Y")
    ax.title(human_time(opts))
