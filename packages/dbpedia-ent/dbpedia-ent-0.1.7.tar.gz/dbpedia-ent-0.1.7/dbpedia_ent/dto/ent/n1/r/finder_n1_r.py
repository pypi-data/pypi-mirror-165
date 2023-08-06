
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1r(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'r_':
            from dbpedia_ent.dto.ent.n1.r import d_trie_r_
            return d_trie_r_

        if ftc == 'ra':
            from dbpedia_ent.dto.ent.n1.r import d_trie_ra
            return d_trie_ra

        if ftc == 'rb':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rb
            return d_trie_rb

        if ftc == 'rc':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rc
            return d_trie_rc

        if ftc == 'rd':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rd
            return d_trie_rd

        if ftc == 're':
            from dbpedia_ent.dto.ent.n1.r import d_trie_re
            return d_trie_re

        if ftc == 'rf':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rf
            return d_trie_rf

        if ftc == 'rg':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rg
            return d_trie_rg

        if ftc == 'rh':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rh
            return d_trie_rh

        if ftc == 'ri':
            from dbpedia_ent.dto.ent.n1.r import d_trie_ri
            return d_trie_ri

        if ftc == 'rj':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rj
            return d_trie_rj

        if ftc == 'rk':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rk
            return d_trie_rk

        if ftc == 'rl':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rl
            return d_trie_rl

        if ftc == 'rm':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rm
            return d_trie_rm

        if ftc == 'rn':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rn
            return d_trie_rn

        if ftc == 'ro':
            from dbpedia_ent.dto.ent.n1.r import d_trie_ro
            return d_trie_ro

        if ftc == 'rp':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rp
            return d_trie_rp

        if ftc == 'rq':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rq
            return d_trie_rq

        if ftc == 'rr':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rr
            return d_trie_rr

        if ftc == 'rs':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rs
            return d_trie_rs

        if ftc == 'rt':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rt
            return d_trie_rt

        if ftc == 'ru':
            from dbpedia_ent.dto.ent.n1.r import d_trie_ru
            return d_trie_ru

        if ftc == 'rv':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rv
            return d_trie_rv

        if ftc == 'rw':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rw
            return d_trie_rw

        if ftc == 'rx':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rx
            return d_trie_rx

        if ftc == 'ry':
            from dbpedia_ent.dto.ent.n1.r import d_trie_ry
            return d_trie_ry

        if ftc == 'rz':
            from dbpedia_ent.dto.ent.n1.r import d_trie_rz
            return d_trie_rz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
