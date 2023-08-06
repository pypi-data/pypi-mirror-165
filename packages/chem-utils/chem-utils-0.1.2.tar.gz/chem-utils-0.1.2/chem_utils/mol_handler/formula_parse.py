#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/8/23 10:45
# @Author  : zhangbc0315@outlook.com
# @File    : formula_parse.py
# @Software: PyCharm

import re

from chem_utils.atom_handler.atom_parse import AtomParse


class FormulaParse:

    _pattern_token = r"([A-Z][a-z]?)[^a-z]"

    @classmethod
    def split_to_tokens(cls, text: str):
        return re.findall(cls._pattern_token, text)

    @classmethod
    def parse_formula(cls, formula: str):
        tokens = cls.split_to_tokens(formula)
        atomic_nums = [AtomParse.symbol_to_atomic_num(token) for token in tokens]
        symbols = []
        for token, atomic_num in zip(tokens, atomic_nums):
            if atomic_num is not None:
                symbols.append(token)
        if len(symbols) < len(tokens) and all([len(s) == 1 for s in symbols]):
            return []
        else:
            return symbols


if __name__ == "__main__":
    # res = FormulaParse.split_to_tokens("NOVELTY-The")
    res = FormulaParse.parse_formula("NOVELTY-The")
    print(res)
