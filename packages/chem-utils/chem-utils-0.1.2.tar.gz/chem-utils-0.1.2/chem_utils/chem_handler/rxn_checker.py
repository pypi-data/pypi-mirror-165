#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 14:37
# @Author  : zhangbc0315@outlook.com
# @File    : rxn_checker.py
# @Software: PyCharm

from rdkit.Chem.AllChem import ChemicalReaction
from rdkit.Chem.rdchem import Mol


class RxnChecker:

    @classmethod
    def _get_all_map_nums_in_mols(cls, mols: [Mol]) -> [int]:
        map_nums = []
        for mol in mols:
            for atom in mol.GetAtoms():
                map_nums.append(atom.GetAtomMapNum())
        return map_nums

    @classmethod
    def is_mapped_enough(cls, rdrxn: ChemicalReaction):
        all_rs_map_nums = cls._get_all_map_nums_in_mols(rdrxn.GetReactants())
        for product in rdrxn.GetProducts():
            for p_atom in product.GetAtoms():
                if p_atom.GetAtomMapNum() == 0:
                    return False
                elif p_atom.GetAtomMapNum() not in all_rs_map_nums:
                    return False
        return True


if __name__ == "__main__":
    pass
