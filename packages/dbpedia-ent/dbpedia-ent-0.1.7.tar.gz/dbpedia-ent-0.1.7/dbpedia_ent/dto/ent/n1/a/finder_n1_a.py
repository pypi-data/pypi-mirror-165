
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1a(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'a_':
            from dbpedia_ent.dto.ent.n1.a import d_trie_a_
            return d_trie_a_

        if ftc == 'aa':
            from dbpedia_ent.dto.ent.n1.a import d_trie_aa
            return d_trie_aa

        if ftc == 'ab':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ab
            return d_trie_ab

        if ftc == 'ac':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ac
            return d_trie_ac

        if ftc == 'ad':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ad
            return d_trie_ad

        if ftc == 'ae':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ae
            return d_trie_ae

        if ftc == 'af':
            from dbpedia_ent.dto.ent.n1.a import d_trie_af
            return d_trie_af

        if ftc == 'ag':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ag
            return d_trie_ag

        if ftc == 'ah':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ah
            return d_trie_ah

        if ftc == 'ai':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ai
            return d_trie_ai

        if ftc == 'aj':
            from dbpedia_ent.dto.ent.n1.a import d_trie_aj
            return d_trie_aj

        if ftc == 'ak':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ak
            return d_trie_ak

        if ftc == 'al':
            from dbpedia_ent.dto.ent.n1.a import d_trie_al
            return d_trie_al

        if ftc == 'am':
            from dbpedia_ent.dto.ent.n1.a import d_trie_am
            return d_trie_am

        if ftc == 'an':
            from dbpedia_ent.dto.ent.n1.a import d_trie_an
            return d_trie_an

        if ftc == 'ao':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ao
            return d_trie_ao

        if ftc == 'ap':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ap
            return d_trie_ap

        if ftc == 'aq':
            from dbpedia_ent.dto.ent.n1.a import d_trie_aq
            return d_trie_aq

        if ftc == 'ar':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ar
            return d_trie_ar

        if ftc == 'as':
            from dbpedia_ent.dto.ent.n1.a import d_trie_as
            return d_trie_as

        if ftc == 'at':
            from dbpedia_ent.dto.ent.n1.a import d_trie_at
            return d_trie_at

        if ftc == 'au':
            from dbpedia_ent.dto.ent.n1.a import d_trie_au
            return d_trie_au

        if ftc == 'av':
            from dbpedia_ent.dto.ent.n1.a import d_trie_av
            return d_trie_av

        if ftc == 'aw':
            from dbpedia_ent.dto.ent.n1.a import d_trie_aw
            return d_trie_aw

        if ftc == 'ax':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ax
            return d_trie_ax

        if ftc == 'ay':
            from dbpedia_ent.dto.ent.n1.a import d_trie_ay
            return d_trie_ay

        if ftc == 'az':
            from dbpedia_ent.dto.ent.n1.a import d_trie_az
            return d_trie_az


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
