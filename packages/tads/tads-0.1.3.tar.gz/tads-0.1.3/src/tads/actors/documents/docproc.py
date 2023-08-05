from .utils import find_row, handle_data_file, save_df_as
from glob import glob
from typing import List

import numpy as np
import pandas as pd


class DocumentProcessor(object):
    data: dict
    df: pd.DataFrame

    def __init__(self, pattern, query, actions=None, cols=None, groups=None):
        self.actions: dict = actions
        self.groups: List[str] = groups
        self.pattern: str = pattern
        self.query: str = query
        self.cols: List[str] = cols

    def __call__(self, save_as: str) -> pd.DataFrame:
        self.clean()
        save_df_as(self.df, save_as)
        return self.df

    def aggregate(self, df) -> pd.DataFrame:
        print("Aggregating columns..")
        return df.agg(self.actions)

    def clean(self) -> pd.DataFrame:
        df = self.df = self.collect_into()
        if self.groups:
            df = self.group(df)
        if self.actions:
            df = self.aggregate(df)
        df = df.drop([i for i in df.columns if i not in self.cols], axis=1)
        df.replace('', np.nan, inplace=True)
        self.data, self.df = df.to_dict(), df[:]
        return self.df

    def collect(self, **kwargs) -> list:
        if self.query:
            return [handle_data_file(f, skiprows=find_row(f, self.query), **kwargs) for f in glob(self.pattern)]
        else:
            return [handle_data_file(f, **kwargs) for f in glob(self.pattern)]

    def collect_into(self, ignore_index: bool = True, **kwargs) -> pd.DataFrame:
        return pd.concat(self.collect(), ignore_index=ignore_index, **kwargs)

    def divide(self, cols: List[str], by: float) -> pd.DataFrame:
        for col in cols:
            self.df[col] /= by
        return self.df

    def drop(self, *args, axis=1, inplace=True, **kwargs):
        self.df.drop(args, axis=axis, inplace=inplace, **kwargs)
        return self.df

    def group(self, df, as_index: bool = False, **kwargs) -> pd.DataFrame:
        print("Grouping data...")
        return df.groupby(self.groups, as_index=as_index, **kwargs)

    def rename(self, col_map: dict) -> pd.DataFrame:
        self.df.rename(col_map, axis=1, inplace=True)
        return self.df

    def replace(self, to_replace='', value=np.nan, inplace: bool = True, **kwargs):
        self.df.replace(to_replace, value, inplace=inplace, **kwargs)
        return self.df
