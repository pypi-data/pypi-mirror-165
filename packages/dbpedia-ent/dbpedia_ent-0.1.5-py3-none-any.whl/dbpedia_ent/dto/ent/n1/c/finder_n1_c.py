
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1c(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'c_':
            from dbpedia_ent.dto.ent.n1.c import d_trie_c_
            return d_trie_c_

        if ftc == 'ca':
            from dbpedia_ent.dto.ent.n1.c import d_trie_ca
            return d_trie_ca

        if ftc == 'cb':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cb
            return d_trie_cb

        if ftc == 'cc':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cc
            return d_trie_cc

        if ftc == 'cd':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cd
            return d_trie_cd

        if ftc == 'ce':
            from dbpedia_ent.dto.ent.n1.c import d_trie_ce
            return d_trie_ce

        if ftc == 'cf':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cf
            return d_trie_cf

        if ftc == 'cg':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cg
            return d_trie_cg

        if ftc == 'ch':
            from dbpedia_ent.dto.ent.n1.c import d_trie_ch
            return d_trie_ch

        if ftc == 'ci':
            from dbpedia_ent.dto.ent.n1.c import d_trie_ci
            return d_trie_ci

        if ftc == 'cj':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cj
            return d_trie_cj

        if ftc == 'ck':
            from dbpedia_ent.dto.ent.n1.c import d_trie_ck
            return d_trie_ck

        if ftc == 'cl':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cl
            return d_trie_cl

        if ftc == 'cm':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cm
            return d_trie_cm

        if ftc == 'cn':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cn
            return d_trie_cn

        if ftc == 'co':
            from dbpedia_ent.dto.ent.n1.c import d_trie_co
            return d_trie_co

        if ftc == 'cp':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cp
            return d_trie_cp

        if ftc == 'cq':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cq
            return d_trie_cq

        if ftc == 'cr':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cr
            return d_trie_cr

        if ftc == 'cs':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cs
            return d_trie_cs

        if ftc == 'ct':
            from dbpedia_ent.dto.ent.n1.c import d_trie_ct
            return d_trie_ct

        if ftc == 'cu':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cu
            return d_trie_cu

        if ftc == 'cv':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cv
            return d_trie_cv

        if ftc == 'cw':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cw
            return d_trie_cw

        if ftc == 'cx':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cx
            return d_trie_cx

        if ftc == 'cy':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cy
            return d_trie_cy

        if ftc == 'cz':
            from dbpedia_ent.dto.ent.n1.c import d_trie_cz
            return d_trie_cz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
