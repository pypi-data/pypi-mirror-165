#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/8/15 17:15
# @Author  : zbc@mail.ustc.edu.cn
# @File    : rxn_smiles.py
# @Software: PyCharm


from rdkit.Chem import AllChem
from rdkit.Chem.AllChem import ChemicalReaction


class RxnSmiles:

    # region ===== rdrxn_from_indigo_smiles =====

    @classmethod
    def _parse_indigo_tag(cls, indigo_tags_str: str) -> [[int]]:
        # for tags in indigo_tags_str.split(','):
        #     pass
        if len(indigo_tags_str) == 0:
            return []
        indigo_tags = [[int(tag) for tag in tags.split('.')] for tags in indigo_tags_str.split(',')]
        return indigo_tags

    @classmethod
    def _split_smiles_by_indigo_tags(cls, rxn_smiles: str, indigo_tags: [[int]]) -> ([str], [str]):
        rs_smiles, cs_smiles, ps_smiles = rxn_smiles.split('>')
        r_smileses = rs_smiles.split('.')
        p_smileses = ps_smiles.split('.')
        cs_smileses = cs_smiles.split('.')
        all_smileses = r_smileses.copy()
        all_smileses.extend(cs_smileses)
        all_smileses.extend(p_smileses)
        num_rs = len(r_smileses)
        num_cs = len(cs_smileses)
        rs = []
        ps = []
        all_tags = []
        for tags in indigo_tags:
            all_tags.extend(tags)
            mol_smileses = []

            for tag in tags:
                mol_smileses.append(all_smileses[tag])
            if tags[0] >= num_rs + num_cs:
                ps.append('.'.join(mol_smileses))
            elif tags[0] < num_rs:
                rs.append('.'.join(mol_smileses))
        for i, smiles in enumerate(all_smileses):
            if i in all_tags:
                continue
            if i >= num_rs:
                ps.append(smiles)
            else:
                rs.append(smiles)
        return rs, ps

    @classmethod
    def _rdrxn_from_smileses(cls, r_smileses: [str], p_smileses: [str]):
        rdrxn = ChemicalReaction()
        for r_smiles in r_smileses:
            rdrxn.AddReactantTemplate(AllChem.MolFromSmiles(r_smiles))
        for p_smiles in p_smileses:
            rdrxn.AddProductTemplate(AllChem.MolFromSmiles(p_smiles))
        return rdrxn

    @classmethod
    def _split_indigo_smiles(cls, indigo_smiles: str) -> (str, str):
        if ' |' in indigo_smiles:
            rxn_smiles, indigo_tags_str = indigo_smiles.split(' |')
            indigo_tags_str = indigo_tags_str.strip('f:')

        else:
            rxn_smiles = indigo_smiles
            indigo_tags_str = ''

        if '^' in indigo_tags_str:
            indigo_tags_str = indigo_tags_str.split('^')[0]

        indigo_tags_str = indigo_tags_str.strip('|')
        indigo_tags_str = indigo_tags_str.strip(',')
        return rxn_smiles, indigo_tags_str

    @classmethod
    def rdrxn_from_indigo_smiles(cls, indigo_smiles: str):
        # print(indigo_smiles)
        rxn_smiles, indigo_tags_str = cls._split_indigo_smiles(indigo_smiles)
        indigo_tags = cls._parse_indigo_tag(indigo_tags_str)
        r_smileses, p_smileses = cls._split_smiles_by_indigo_tags(rxn_smiles, indigo_tags)
        return cls._rdrxn_from_smileses(r_smileses, p_smileses)

    # endregion


if __name__ == "__main__":
    smi = "Br[C:2]1[C:3]([C:17]2[CH:22]=[CH:21][CH:20]=[CH:19][CH:18]=2)=[CH:4][C:5]2[N:10]([CH2:11][CH:12]3[CH2:14][CH2:13]3)[C:9](=[O:15])[CH2:8][O:7][C:6]=2[N:16]=1.CC1(C)C(C)(C)OB([C:31]2[CH:45]=[CH:44][C:34]([CH2:35][NH:36][C:37](=[O:43])[O:38][C:39]([CH3:42])([CH3:41])[CH3:40])=[CH:33][CH:32]=2)O1.C(=O)([O-])[O-].[Cs+].[Cs+]>O1CCOCC1.O>[CH:12]1([CH2:11][N:10]2[C:9](=[O:15])[CH2:8][O:7][C:6]3[N:16]=[C:2]([C:31]4[CH:45]=[CH:44][C:34]([CH2:35][NH:36][C:37](=[O:43])[O:38][C:39]([CH3:40])([CH3:41])[CH3:42])=[CH:33][CH:32]=4)[C:3]([C:17]4[CH:22]=[CH:21][CH:20]=[CH:19][CH:18]=4)=[CH:4][C:5]2=3)[CH2:14][CH2:13]1 |f:2.3.4|"
    smi = "Cl.[C:2]1(=O)C2(CCNCC2)CCN1.C(N(CC)CC)C.BrC1C=C(S(Cl)(=O)=O)C=C(C(F)(F)F)C=1.Br[C:36]1[CH:37]=[C:38]([S:46]([N:49]2[CH2:59][CH2:58][C:52]3([C:56](=[O:57])[NH:55][CH2:54][CH2:53]3)[CH2:51][CH2:50]2)(=[O:48])=[O:47])[CH:39]=[C:40]([C:42]([F:45])([F:44])[F:43])[CH:41]=1.C(=O)([O-])[O-].[K+].[K+].CB1OB(C)OB(C)O1>ClCCl.O1CCOCC1.C1C=CC([P]([Pd]([P](C2C=CC=CC=2)(C2C=CC=CC=2)C2C=CC=CC=2)([P](C2C=CC=CC=2)(C2C=CC=CC=2)C2C=CC=CC=2)[P](C2C=CC=CC=2)(C2C=CC=CC=2)C2C=CC=CC=2)(C2C=CC=CC=2)C2C=CC=CC=2)=CC=1>[CH3:2][C:36]1[CH:37]=[C:38]([S:46]([N:49]2[CH2:50][CH2:51][C:52]3([C:56](=[O:57])[NH:55][CH2:54][CH2:53]3)[CH2:58][CH2:59]2)(=[O:47])=[O:48])[CH:39]=[C:40]([C:42]([F:44])([F:45])[F:43])[CH:41]=1 |f:0.1,5.6.7,^1:87,89,108,127|"
    RxnSmiles.rdrxn_from_indigo_smiles(smi)
