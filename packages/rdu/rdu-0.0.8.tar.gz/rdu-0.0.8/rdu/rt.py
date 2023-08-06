#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/5 21:49
# @Author  : zbc@mail.ustc.edu.cn
# @File    : rt.py
# @Software: PyCharm

import pandas as pd


class RT:

    def __init__(self, ser: pd.Series):
        self.rt_code: str = ser['rt_code']
        self.rxn_template: str = ser['rxn_template']
        self.num_of_covered_rxn: int = ser['num_of_covered_rxn']


if __name__ == "__main__":
    pass
