
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1g(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'g_':
            from dbpedia_ent.dto.ent.n1.g import d_trie_g_
            return d_trie_g_

        if ftc == 'ga':
            from dbpedia_ent.dto.ent.n1.g import d_trie_ga
            return d_trie_ga

        if ftc == 'gb':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gb
            return d_trie_gb

        if ftc == 'gc':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gc
            return d_trie_gc

        if ftc == 'gd':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gd
            return d_trie_gd

        if ftc == 'ge':
            from dbpedia_ent.dto.ent.n1.g import d_trie_ge
            return d_trie_ge

        if ftc == 'gf':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gf
            return d_trie_gf

        if ftc == 'gg':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gg
            return d_trie_gg

        if ftc == 'gh':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gh
            return d_trie_gh

        if ftc == 'gi':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gi
            return d_trie_gi

        if ftc == 'gj':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gj
            return d_trie_gj

        if ftc == 'gk':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gk
            return d_trie_gk

        if ftc == 'gl':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gl
            return d_trie_gl

        if ftc == 'gm':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gm
            return d_trie_gm

        if ftc == 'gn':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gn
            return d_trie_gn

        if ftc == 'go':
            from dbpedia_ent.dto.ent.n1.g import d_trie_go
            return d_trie_go

        if ftc == 'gp':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gp
            return d_trie_gp

        if ftc == 'gq':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gq
            return d_trie_gq

        if ftc == 'gr':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gr
            return d_trie_gr

        if ftc == 'gs':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gs
            return d_trie_gs

        if ftc == 'gt':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gt
            return d_trie_gt

        if ftc == 'gu':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gu
            return d_trie_gu

        if ftc == 'gv':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gv
            return d_trie_gv

        if ftc == 'gw':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gw
            return d_trie_gw

        if ftc == 'gx':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gx
            return d_trie_gx

        if ftc == 'gy':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gy
            return d_trie_gy

        if ftc == 'gz':
            from dbpedia_ent.dto.ent.n1.g import d_trie_gz
            return d_trie_gz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
