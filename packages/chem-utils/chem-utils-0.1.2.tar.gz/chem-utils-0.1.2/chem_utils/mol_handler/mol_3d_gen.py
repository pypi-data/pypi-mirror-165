#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/8/25 15:07
# @Author  : zhangbc0315@outlook.com
# @File    : mol_3d_gen.py
# @Software: PyCharm

from rdkit.Chem import AllChem


class Mol3DGen:

    @classmethod
    def gen_3d(cls, mol_smi: str):
        rdmol = AllChem.MolFromSmiles(mol_smi)
        rdmol = AllChem.AddHs(rdmol)
        AllChem.MMFFSanitizeMolecule(rdmol)
        AllChem.EmbedMolecule(rdmol)
        conf = rdmol.GetConformer()
        positions = []
        for atom, position in zip(rdmol.GetAtoms(), conf.GetPositions()):
            positions.append((atom.GetSymbol(), position.tolist()))
        return positions


if __name__ == "__main__":
    print(Mol3DGen.gen_3d('c1ccccc1'))
