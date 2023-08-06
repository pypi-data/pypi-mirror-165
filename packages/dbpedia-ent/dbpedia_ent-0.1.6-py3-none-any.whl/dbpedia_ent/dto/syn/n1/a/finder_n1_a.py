
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1a(object):

    def _get_trie(self,
                  ftc: str) -> dict:

        if ftc == 'aa':
            from dbpedia_ent.dto.syn.n1.a import d_rev_aa
            return d_rev_aa

        if ftc == 'ab':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ab
            return d_rev_ab

        if ftc == 'ac':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ac
            return d_rev_ac

        if ftc == 'ad':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ad
            return d_rev_ad

        if ftc == 'ae':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ae
            return d_rev_ae

        if ftc == 'af':
            from dbpedia_ent.dto.syn.n1.a import d_rev_af
            return d_rev_af

        if ftc == 'ag':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ag
            return d_rev_ag

        if ftc == 'ah':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ah
            return d_rev_ah

        if ftc == 'ai':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ai
            return d_rev_ai

        if ftc == 'aj':
            from dbpedia_ent.dto.syn.n1.a import d_rev_aj
            return d_rev_aj

        if ftc == 'ak':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ak
            return d_rev_ak

        if ftc == 'al':
            from dbpedia_ent.dto.syn.n1.a import d_rev_al
            return d_rev_al

        if ftc == 'am':
            from dbpedia_ent.dto.syn.n1.a import d_rev_am
            return d_rev_am

        if ftc == 'an':
            from dbpedia_ent.dto.syn.n1.a import d_rev_an
            return d_rev_an

        if ftc == 'ao':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ao
            return d_rev_ao

        if ftc == 'ap':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ap
            return d_rev_ap

        if ftc == 'aq':
            from dbpedia_ent.dto.syn.n1.a import d_rev_aq
            return d_rev_aq

        if ftc == 'ar':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ar
            return d_rev_ar

        if ftc == 'as':
            from dbpedia_ent.dto.syn.n1.a import d_rev_as
            return d_rev_as

        if ftc == 'at':
            from dbpedia_ent.dto.syn.n1.a import d_rev_at
            return d_rev_at

        if ftc == 'au':
            from dbpedia_ent.dto.syn.n1.a import d_rev_au
            return d_rev_au

        if ftc == 'av':
            from dbpedia_ent.dto.syn.n1.a import d_rev_av
            return d_rev_av

        if ftc == 'aw':
            from dbpedia_ent.dto.syn.n1.a import d_rev_aw
            return d_rev_aw

        if ftc == 'ax':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ax
            return d_rev_ax

        if ftc == 'ay':
            from dbpedia_ent.dto.syn.n1.a import d_rev_ay
            return d_rev_ay

        if ftc == 'az':
            from dbpedia_ent.dto.syn.n1.a import d_rev_az
            return d_rev_az

    def find_canon(self,
                   input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
