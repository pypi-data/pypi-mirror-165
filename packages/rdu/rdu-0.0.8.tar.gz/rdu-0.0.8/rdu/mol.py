#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 15:03
# @Author  : zbc@mail.ustc.edu.cn
# @File    : mol.py
# @Software: PyCharm

import pandas as pd


class Mol:

    def __init__(self, ser: pd.Series):
        self.id: int = ser['id']
        self.mol_code: str = ser['mol_code']
        # self.names: [str] = []
        self.inchi: str = ser['inchi']
        self.smiles: str = ser['smiles']


if __name__ == "__main__":
    pass
