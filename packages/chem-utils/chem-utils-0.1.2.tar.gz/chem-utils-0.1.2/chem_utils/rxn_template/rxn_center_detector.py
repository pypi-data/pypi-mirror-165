#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 10:42
# @Author  : zhangbc0315@outlook.com
# @File    : rxn_center_detector.py
# @Software: PyCharm

from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Atom, Bond, Mol

from chem_utils.chem_handler import AtomHandler, MolHandler


class RxnCenterDetector:

    # region ===== assign special atoms =====

    @classmethod
    def _is_atom_dropped_by_product(cls, map_num: int, product: Mol) -> bool:
        return map_num is None or map_num == 0 \
               or not MolHandler.contain_atom_with_map_num_in_mols([product], map_num)

    @classmethod
    def _is_atom_dropped(cls, map_num: int, rxn: AllChem.ChemicalReaction) -> bool:
        return map_num is None or map_num == 0 \
               or not MolHandler.contain_atom_with_map_num_in_mols(rxn.GetProducts(), map_num)

    @classmethod
    def _has_same_num_neighbor(cls, r_atom: Atom, p_atom: Atom) -> bool:
        return len(r_atom.GetNeighbors()) == len(p_atom.GetNeighbors())

    @classmethod
    def _get_nbr_with_map_num(cls, atom: Atom, map_num: int) -> Atom:
        for nbr_atom in atom.GetNeighbors():
            if nbr_atom.GetAtomMapNum() == map_num:
                return nbr_atom
        return None

    @classmethod
    def _is_same_atoms(cls, atom1: Atom, atom2: Atom) -> bool:
        return atom1.GetAtomicNum() == atom2.GetAtomicNum() \
               and atom1.GetNumRadicalElectrons() == atom2.GetNumRadicalElectrons() \
               and len(atom1.GetNeighbors()) == len(atom2.GetNeighbors())

    @classmethod
    def _is_same_bond(cls, bond1: Bond, bond2: Bond):
        return bond1.GetBondType() == bond2.GetBondType()

    @classmethod
    def _has_same_neighbor_atom_with_same_bond(cls, r_atom: Atom, p_atom: Atom) -> bool:
        for r_nbr_atom in r_atom.GetNeighbors():
            p_nbr_atom = cls._get_nbr_with_map_num(p_atom, r_nbr_atom.GetAtomMapNum())
            if p_nbr_atom is None:
                return False
            r_bond = r_atom.GetOwningMol().GetBondBetweenAtoms(r_atom.GetIdx(), r_nbr_atom.GetIdx())
            p_bond = p_atom.GetOwningMol().GetBondBetweenAtoms(p_atom.GetIdx(), p_nbr_atom.GetIdx())
            if not cls._is_same_bond(r_bond, p_bond):
                return False
        return True

    @classmethod
    def _is_atom_reacted(cls, r_atom: Atom, p_atom: Atom) -> bool:
        if not cls._is_same_atoms(r_atom, p_atom):
            return True
        if not cls._has_same_neighbor_atom_with_same_bond(r_atom, p_atom):
            return True
        return False

    @classmethod
    def _assign_dropped_and_reacted_atoms_in_rxn(cls, rxn: AllChem.ChemicalReaction):
        for reactant in rxn.GetReactants():
            for atom in reactant.GetAtoms():
                map_num = atom.GetAtomMapNum()
                if cls._is_atom_dropped(map_num, rxn):
                    AtomHandler.set_atom_is_dropped(atom)
                    atom.SetAtomMapNum(0)
                else:
                    p_atom = list(MolHandler.query_atoms_with_map_num_in_mols(rxn.GetProducts(), map_num))[0]
                    if cls._is_atom_reacted(atom, p_atom):
                        AtomHandler.set_atom_is_reacted(atom)
                        AtomHandler.set_atom_is_reacted(p_atom)

    @classmethod
    def get_center_atom_idxes(cls, reactant: Mol, product: Mol):
        center_atom_idxes = []
        for atom in reactant.GetAtoms():
            map_num = atom.GetAtomMapNum()
            if cls._is_atom_dropped_by_product(map_num, product):
                center_atom_idxes.append(atom.GetIdx())
            else:
                p_atom = list(MolHandler.query_atoms_with_map_num(product, map_num))[0]
                if cls._is_atom_reacted(atom, p_atom):
                    center_atom_idxes.append(atom.GetIdx())
        return center_atom_idxes

    # endregion


if __name__ == "__main__":
    pass
