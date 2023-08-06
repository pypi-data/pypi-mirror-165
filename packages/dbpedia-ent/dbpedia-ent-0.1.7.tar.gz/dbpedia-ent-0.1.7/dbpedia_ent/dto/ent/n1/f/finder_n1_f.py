
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1f(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'f_':
            from dbpedia_ent.dto.ent.n1.f import d_trie_f_
            return d_trie_f_

        if ftc == 'fa':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fa
            return d_trie_fa

        if ftc == 'fb':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fb
            return d_trie_fb

        if ftc == 'fc':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fc
            return d_trie_fc

        if ftc == 'fd':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fd
            return d_trie_fd

        if ftc == 'fe':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fe
            return d_trie_fe

        if ftc == 'ff':
            from dbpedia_ent.dto.ent.n1.f import d_trie_ff
            return d_trie_ff

        if ftc == 'fg':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fg
            return d_trie_fg

        if ftc == 'fh':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fh
            return d_trie_fh

        if ftc == 'fi':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fi
            return d_trie_fi

        if ftc == 'fj':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fj
            return d_trie_fj

        if ftc == 'fk':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fk
            return d_trie_fk

        if ftc == 'fl':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fl
            return d_trie_fl

        if ftc == 'fm':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fm
            return d_trie_fm

        if ftc == 'fn':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fn
            return d_trie_fn

        if ftc == 'fo':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fo
            return d_trie_fo

        if ftc == 'fp':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fp
            return d_trie_fp

        if ftc == 'fq':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fq
            return d_trie_fq

        if ftc == 'fr':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fr
            return d_trie_fr

        if ftc == 'fs':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fs
            return d_trie_fs

        if ftc == 'ft':
            from dbpedia_ent.dto.ent.n1.f import d_trie_ft
            return d_trie_ft

        if ftc == 'fu':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fu
            return d_trie_fu

        if ftc == 'fv':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fv
            return d_trie_fv

        if ftc == 'fw':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fw
            return d_trie_fw

        if ftc == 'fx':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fx
            return d_trie_fx

        if ftc == 'fy':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fy
            return d_trie_fy

        if ftc == 'fz':
            from dbpedia_ent.dto.ent.n1.f import d_trie_fz
            return d_trie_fz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
