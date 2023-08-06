#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/8/22 10:48
# @Author  : zhangbc0315@outlook.com
# @File    : mol_smiles.py
# @Software: PyCharm
import copy

from rdkit.Chem.rdchem import Mol
from rdkit.Chem import AllChem


class MolSmiles:

    @classmethod
    def remove_map_num(cls, smiles: str) -> str:
        rdmol = AllChem.MolFromSmarts(smiles)
        for atom in rdmol.GetAtoms():
            atom.SetAtomMapNum(0)
        return AllChem.MolToSmiles(rdmol)

    @classmethod
    def get_smiles_without_map_num(cls, rdmol: Mol) -> str:
        _rdmol = copy.deepcopy(rdmol)
        for atom in _rdmol.GetAtoms():
            atom.SetAtomMapNum(0)
        return AllChem.MolToSmiles(_rdmol)


if __name__ == "__main__":
    print(MolSmiles.remove_map_num('[c:1][c:2]=N'))
