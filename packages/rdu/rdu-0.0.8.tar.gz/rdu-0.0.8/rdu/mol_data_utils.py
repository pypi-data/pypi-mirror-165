#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 15:48
# @Author  : zbc@mail.ustc.edu.cn
# @File    : mol_utils.py
# @Software: PyCharm

import pandas as pd

from rdu.mol import Mol


class MolDataUtils:

    def __init__(self, mol_data_fp: str):
        self._mol_df = pd.read_csv(mol_data_fp, sep='\t', encoding='utf-8')

    def num_mol(self) -> int:
        return len(self._mol_df)

    def get_mol_with_code(self, mol_code: str) -> Mol:
        query_df = self._mol_df.query(f"mol_code=='{mol_code}'")
        if len(query_df) == 0:
            return None
        idx = query_df.index[0]
        return Mol(query_df.loc[idx])


if __name__ == "__main__":
    pass
