from django_pandas.io import read_frame
import pandas as pd
import numpy as np
from .models import SpaceStatus, SpaceStatusPrediction
from django.utils import timezone

def human_time(options):
    days_names = ["Lundi", "Mardi", "Mercredi",
                  "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    res = "Ouverture de UrLab: "
    if 'tomorrow' in options:
        res += " demain"
    else:
        res += " aujourd'hui"
    return res


def weekday_probs(opts):
    # check today by default
    begin_hour = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if 'tomorrow' in opts:
        begin_hour += timezone.timedelta(days=1)
    end_hour = begin_hour + timezone.timedelta(days=1)
    df = read_frame(SpaceStatusPrediction.objects.filter(time__gte=begin_hour, time__lt=end_hour))
    return df.proba_open


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
    ax.title(human_time(opts))
