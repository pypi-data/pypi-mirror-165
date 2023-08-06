#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/5 21:49
# @Author  : zbc@mail.ustc.edu.cn
# @File    : rt_data_utils.py
# @Software: PyCharm

from typing import Iterator

import pandas as pd

from rdu.rt import RT
from rdu.rxn_data_utils import RxnDataUtils, Rxn


class RTDataUtils:

    def __init__(self, rt_data_fp: str, rt_rxn_link_fp: str, rxn_data_utils: RxnDataUtils):
        self._rt_data_df = pd.read_csv(rt_data_fp, sep='\t', encoding='utf-8')
        self._rt_rxn_link_df = pd.read_csv(rt_rxn_link_fp, sep='\t', encoding='utf-8')
        self._rxn_data_utils = rxn_data_utils

    def num_rt(self) -> int:
        return len(self._rt_data_df)

    def get_rts(self) -> Iterator[RT]:
        for _, row in self._rt_data_df.iterrows():
            yield RT(row)

    def get_rxn_by_rt_code(self, rt_code: str, rt_type: str) -> Iterator[Rxn]:
        if rt_type not in ['rct', 'ret']:
            raise ValueError(f"rt_type应为 'rct'或'ret' 但却得到 '{rt_type}'")
        rt_code_col = f"{rt_type}_code"
        query_df = self._rt_rxn_link_df.query(f"{rt_code_col}=='{rt_code}'")
        for _, row in query_df.iterrows():
            rxn_code = row['rxn_code']
            yield self._rxn_data_utils.get_rxn_by_code(rxn_code)

    def get_rt_by_rt_code(self, rt_code: str) -> RT:
        query_df = self._rt_data_df.query(f"rt_code=='{rt_code}'")
        if len(query_df) == 0:
            return None
        idx = query_df.index[0]
        return RT(query_df.loc[idx])


if __name__ == "__main__":
    pass
