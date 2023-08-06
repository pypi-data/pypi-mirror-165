
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1m(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'm_':
            from dbpedia_ent.dto.ent.n1.m import d_trie_m_
            return d_trie_m_

        if ftc == 'ma':
            from dbpedia_ent.dto.ent.n1.m import d_trie_ma
            return d_trie_ma

        if ftc == 'mb':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mb
            return d_trie_mb

        if ftc == 'mc':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mc
            return d_trie_mc

        if ftc == 'md':
            from dbpedia_ent.dto.ent.n1.m import d_trie_md
            return d_trie_md

        if ftc == 'me':
            from dbpedia_ent.dto.ent.n1.m import d_trie_me
            return d_trie_me

        if ftc == 'mf':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mf
            return d_trie_mf

        if ftc == 'mg':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mg
            return d_trie_mg

        if ftc == 'mh':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mh
            return d_trie_mh

        if ftc == 'mi':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mi
            return d_trie_mi

        if ftc == 'mj':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mj
            return d_trie_mj

        if ftc == 'mk':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mk
            return d_trie_mk

        if ftc == 'ml':
            from dbpedia_ent.dto.ent.n1.m import d_trie_ml
            return d_trie_ml

        if ftc == 'mm':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mm
            return d_trie_mm

        if ftc == 'mn':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mn
            return d_trie_mn

        if ftc == 'mo':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mo
            return d_trie_mo

        if ftc == 'mp':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mp
            return d_trie_mp

        if ftc == 'mq':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mq
            return d_trie_mq

        if ftc == 'mr':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mr
            return d_trie_mr

        if ftc == 'ms':
            from dbpedia_ent.dto.ent.n1.m import d_trie_ms
            return d_trie_ms

        if ftc == 'mt':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mt
            return d_trie_mt

        if ftc == 'mu':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mu
            return d_trie_mu

        if ftc == 'mv':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mv
            return d_trie_mv

        if ftc == 'mw':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mw
            return d_trie_mw

        if ftc == 'mx':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mx
            return d_trie_mx

        if ftc == 'my':
            from dbpedia_ent.dto.ent.n1.m import d_trie_my
            return d_trie_my

        if ftc == 'mz':
            from dbpedia_ent.dto.ent.n1.m import d_trie_mz
            return d_trie_mz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
