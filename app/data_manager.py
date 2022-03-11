from enum import Enum
from typing import Callable

import numpy as np
import pandas as pd


class EmptyFiller(Enum):
    delete = 1
    minimum = 2
    maximum = 3
    avg = 4


class AnomalyFiller(Enum):
    delete = 1
    log = 2
    avg = 4


class DummyDataManager:

    def preprocess_data(self, data: pd.Dataframe, fill_empty: EmptyFiller, fill_anomaly: AnomalyFiller, normalize):
        if fill_empty is EmptyFiller.delete:
            data.replace('', np.nan, inplace=True)
            data.dropna(inplace=True)
        elif fill_empty is EmptyFiller.minimum:
            data.fillna(data.min(), inplace=True)
        elif fill_empty is EmptyFiller.maximum:
            data.fillna(data.max(), inplace=True)
        elif fill_empty is EmptyFiller.avg:
            data.fillna(data.avg(), inplace=True)

        return data

    def process_data(self, data: pd.Dataframe, process_function: Callable):
        return process_function(data)
