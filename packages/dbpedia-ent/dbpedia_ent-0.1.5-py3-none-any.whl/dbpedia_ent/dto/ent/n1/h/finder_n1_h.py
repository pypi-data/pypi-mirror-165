
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1h(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'h_':
            from dbpedia_ent.dto.ent.n1.h import d_trie_h_
            return d_trie_h_

        if ftc == 'ha':
            from dbpedia_ent.dto.ent.n1.h import d_trie_ha
            return d_trie_ha

        if ftc == 'hb':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hb
            return d_trie_hb

        if ftc == 'hc':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hc
            return d_trie_hc

        if ftc == 'hd':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hd
            return d_trie_hd

        if ftc == 'he':
            from dbpedia_ent.dto.ent.n1.h import d_trie_he
            return d_trie_he

        if ftc == 'hf':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hf
            return d_trie_hf

        if ftc == 'hg':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hg
            return d_trie_hg

        if ftc == 'hh':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hh
            return d_trie_hh

        if ftc == 'hi':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hi
            return d_trie_hi

        if ftc == 'hj':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hj
            return d_trie_hj

        if ftc == 'hk':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hk
            return d_trie_hk

        if ftc == 'hl':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hl
            return d_trie_hl

        if ftc == 'hm':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hm
            return d_trie_hm

        if ftc == 'hn':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hn
            return d_trie_hn

        if ftc == 'ho':
            from dbpedia_ent.dto.ent.n1.h import d_trie_ho
            return d_trie_ho

        if ftc == 'hp':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hp
            return d_trie_hp

        if ftc == 'hq':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hq
            return d_trie_hq

        if ftc == 'hr':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hr
            return d_trie_hr

        if ftc == 'hs':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hs
            return d_trie_hs

        if ftc == 'ht':
            from dbpedia_ent.dto.ent.n1.h import d_trie_ht
            return d_trie_ht

        if ftc == 'hu':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hu
            return d_trie_hu

        if ftc == 'hv':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hv
            return d_trie_hv

        if ftc == 'hw':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hw
            return d_trie_hw

        if ftc == 'hx':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hx
            return d_trie_hx

        if ftc == 'hy':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hy
            return d_trie_hy

        if ftc == 'hz':
            from dbpedia_ent.dto.ent.n1.h import d_trie_hz
            return d_trie_hz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
