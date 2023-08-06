
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1l(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'l_':
            from dbpedia_ent.dto.ent.n1.l import d_trie_l_
            return d_trie_l_

        if ftc == 'la':
            from dbpedia_ent.dto.ent.n1.l import d_trie_la
            return d_trie_la

        if ftc == 'lb':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lb
            return d_trie_lb

        if ftc == 'lc':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lc
            return d_trie_lc

        if ftc == 'ld':
            from dbpedia_ent.dto.ent.n1.l import d_trie_ld
            return d_trie_ld

        if ftc == 'le':
            from dbpedia_ent.dto.ent.n1.l import d_trie_le
            return d_trie_le

        if ftc == 'lf':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lf
            return d_trie_lf

        if ftc == 'lg':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lg
            return d_trie_lg

        if ftc == 'lh':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lh
            return d_trie_lh

        if ftc == 'li':
            from dbpedia_ent.dto.ent.n1.l import d_trie_li
            return d_trie_li

        if ftc == 'lj':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lj
            return d_trie_lj

        if ftc == 'lk':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lk
            return d_trie_lk

        if ftc == 'll':
            from dbpedia_ent.dto.ent.n1.l import d_trie_ll
            return d_trie_ll

        if ftc == 'lm':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lm
            return d_trie_lm

        if ftc == 'ln':
            from dbpedia_ent.dto.ent.n1.l import d_trie_ln
            return d_trie_ln

        if ftc == 'lo':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lo
            return d_trie_lo

        if ftc == 'lp':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lp
            return d_trie_lp

        if ftc == 'lq':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lq
            return d_trie_lq

        if ftc == 'lr':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lr
            return d_trie_lr

        if ftc == 'ls':
            from dbpedia_ent.dto.ent.n1.l import d_trie_ls
            return d_trie_ls

        if ftc == 'lt':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lt
            return d_trie_lt

        if ftc == 'lu':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lu
            return d_trie_lu

        if ftc == 'lv':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lv
            return d_trie_lv

        if ftc == 'lw':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lw
            return d_trie_lw

        if ftc == 'lx':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lx
            return d_trie_lx

        if ftc == 'ly':
            from dbpedia_ent.dto.ent.n1.l import d_trie_ly
            return d_trie_ly

        if ftc == 'lz':
            from dbpedia_ent.dto.ent.n1.l import d_trie_lz
            return d_trie_lz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
