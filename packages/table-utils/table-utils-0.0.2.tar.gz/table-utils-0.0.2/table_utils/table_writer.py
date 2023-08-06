#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/8/31 10:40
# @Author  : zhangbc0315@outlook.com
# @File    : table_writer.py
# @Software: PyCharm

import os

import pandas as pd


class TableWriter:

    @classmethod
    def write_tsv_by_df(cls, df: pd.DataFrame, fp: str, mode: str = 'auto', index: bool = False):
        if mode == 'w' or not os.path.exists(fp):
            df.to_csv(fp, sep='\t', encoding='utf-8', index=index)
        elif len(df) > 0:
            df.to_csv(fp, sep='\t', encoding='utf-8', index=index, header=False, mode='a')


if __name__ == "__main__":
    pass
