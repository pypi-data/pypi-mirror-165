
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1u(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'u_':
            from dbpedia_ent.dto.ent.n1.u import d_trie_u_
            return d_trie_u_

        if ftc == 'ua':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ua
            return d_trie_ua

        if ftc == 'ub':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ub
            return d_trie_ub

        if ftc == 'uc':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uc
            return d_trie_uc

        if ftc == 'ud':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ud
            return d_trie_ud

        if ftc == 'ue':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ue
            return d_trie_ue

        if ftc == 'uf':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uf
            return d_trie_uf

        if ftc == 'ug':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ug
            return d_trie_ug

        if ftc == 'uh':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uh
            return d_trie_uh

        if ftc == 'ui':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ui
            return d_trie_ui

        if ftc == 'uj':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uj
            return d_trie_uj

        if ftc == 'uk':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uk
            return d_trie_uk

        if ftc == 'ul':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ul
            return d_trie_ul

        if ftc == 'um':
            from dbpedia_ent.dto.ent.n1.u import d_trie_um
            return d_trie_um

        if ftc == 'un':
            from dbpedia_ent.dto.ent.n1.u import d_trie_un
            return d_trie_un

        if ftc == 'uo':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uo
            return d_trie_uo

        if ftc == 'up':
            from dbpedia_ent.dto.ent.n1.u import d_trie_up
            return d_trie_up

        if ftc == 'uq':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uq
            return d_trie_uq

        if ftc == 'ur':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ur
            return d_trie_ur

        if ftc == 'us':
            from dbpedia_ent.dto.ent.n1.u import d_trie_us
            return d_trie_us

        if ftc == 'ut':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ut
            return d_trie_ut

        if ftc == 'uu':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uu
            return d_trie_uu

        if ftc == 'uv':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uv
            return d_trie_uv

        if ftc == 'uw':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uw
            return d_trie_uw

        if ftc == 'ux':
            from dbpedia_ent.dto.ent.n1.u import d_trie_ux
            return d_trie_ux

        if ftc == 'uy':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uy
            return d_trie_uy

        if ftc == 'uz':
            from dbpedia_ent.dto.ent.n1.u import d_trie_uz
            return d_trie_uz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
