#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 15:03
# @Author  : zbc@mail.ustc.edu.cn
# @File    : rxn.py
# @Software: PyCharm

import pandas as pd

from rdu.mol import Mol


class Rxn:

    def __init__(self, ser: pd.Series):
        self.id = ser['id']
        self.rxn_code = ser['rxn_code']
        self.rxn_mols_code = ser['rxn_mols_code']
        self.reactants_codes = eval(ser['reactants_codes'])
        self.product_code = ser['product_code']
        self.catalysts_codes = eval(ser['catalysts_codes'])
        self.solvents_codes = eval(ser['solvents_codes'])
        self.yield_product = ser['yield_product']
        self.rxn_smiles = ser['rxn_smiles']
        self.create_year = ser['create_year']

        self.reactants: [Mol] = []
        self.products: [Mol] = []
        self.catalysts: [Mol] = []
        self.solvents: [Mol] = []


if __name__ == "__main__":
    pass
