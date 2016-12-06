from django.core.management.base import BaseCommand, CommandError
from space.models import SpaceStatusPrediction, SpaceStatus

from django.utils import timezone

import pandas as pd
from django_pandas.io import read_frame
from math import floor
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import numpy as np

class Command(BaseCommand):
    help = 'Predicts the opening status for the next hour'

    def handle(self, *args, **options):
        # get training data until now
        now_hour = timezone.now().replace(second=0, minute=0, microsecond=0)
        df = read_frame(SpaceStatus.objects.filter(time__lte=now_hour))

        # resample by hour and set correct types
        df = df[['time', 'is_open']].drop_duplicates('time').set_index('time')
        df = df.resample('1H').ffill().dropna()
        df['is_open'] = df['is_open'].astype(np.int32)

        # used later to predict 24 hours in a row
        predictions = df.copy()

        # create features for training data
        df['time'] = df.index
        df['weekday'] = df.time.dt.weekday
        df['hour'] = df.time.dt.hour
        df['openlastweek'] = df.is_open.shift(24*7).fillna(False).astype(np.int32)
        df['openlastday'] = df.is_open.shift(24).fillna(False).astype(np.int32)
        df['openlasthour2'] = df.is_open.shift(2).fillna(False).astype(np.int32)
        df['openlasthour'] = df.is_open.shift(1).fillna(False).astype(np.int32)
        df['weekno'] = df.time.dt.week

        # fit predictor
        X = df[['weekday', 'hour', 'openlastweek', 'openlastday', 'openlasthour2', 'openlasthour', 'weekno']].values
        y = df['is_open'].values
        predictor = RandomForestClassifier(100)
        predictor.fit(X, y)

        # predict the next 24hours
        predict_time = timezone.now().replace(minute=0, second=0, microsecond=0) + timezone.timedelta(hours=1)
        for i in range(0, 24):
            new_time = predict_time + timezone.timedelta(hours=i)
            # create features for prediction
            openlastweek = predictions[predictions.index == new_time + timezone.timedelta(weeks=-1)].reset_index(drop=True)
            openlastday = predictions[predictions.index == new_time + timezone.timedelta(days=-1)].reset_index(drop=True)
            openlasthour2 = predictions[predictions.index == new_time + timezone.timedelta(hours=-2)].reset_index(drop=True)
            openlasthour = predictions[predictions.index == new_time + timezone.timedelta(hours=-1)].reset_index(drop=True)
            predict_features =  [[
                                    new_time.weekday(),
                                    new_time.hour,
                                    openlastweek.loc[0].is_open if openlastweek.size > 0 else 0,
                                    openlastday.loc[0].is_open if openlastday.size > 0 else 0,
                                    openlasthour2.loc[0].is_open if openlasthour2.size > 0 else 0,
                                    openlasthour.loc[0].is_open if openlasthour.size > 0 else 0,
                                    new_time.isocalendar()[1]
                                ]]
            proba_open = predictor.predict_proba(predict_features)[0][1]
            # add current prediction to data to predict further away
            predictions.loc[new_time] = proba_open

            # create or update in db
            ssp = SpaceStatusPrediction.objects.get_or_create(time=new_time, defaults={'proba_open': proba_open})[0]
            ssp.save()