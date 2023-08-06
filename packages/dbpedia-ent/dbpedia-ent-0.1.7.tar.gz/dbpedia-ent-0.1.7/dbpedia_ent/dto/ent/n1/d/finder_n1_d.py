
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1d(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'd_':
            from dbpedia_ent.dto.ent.n1.d import d_trie_d_
            return d_trie_d_

        if ftc == 'da':
            from dbpedia_ent.dto.ent.n1.d import d_trie_da
            return d_trie_da

        if ftc == 'db':
            from dbpedia_ent.dto.ent.n1.d import d_trie_db
            return d_trie_db

        if ftc == 'dc':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dc
            return d_trie_dc

        if ftc == 'dd':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dd
            return d_trie_dd

        if ftc == 'de':
            from dbpedia_ent.dto.ent.n1.d import d_trie_de
            return d_trie_de

        if ftc == 'df':
            from dbpedia_ent.dto.ent.n1.d import d_trie_df
            return d_trie_df

        if ftc == 'dg':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dg
            return d_trie_dg

        if ftc == 'dh':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dh
            return d_trie_dh

        if ftc == 'di':
            from dbpedia_ent.dto.ent.n1.d import d_trie_di
            return d_trie_di

        if ftc == 'dj':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dj
            return d_trie_dj

        if ftc == 'dk':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dk
            return d_trie_dk

        if ftc == 'dl':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dl
            return d_trie_dl

        if ftc == 'dm':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dm
            return d_trie_dm

        if ftc == 'dn':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dn
            return d_trie_dn

        if ftc == 'do':
            from dbpedia_ent.dto.ent.n1.d import d_trie_do
            return d_trie_do

        if ftc == 'dp':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dp
            return d_trie_dp

        if ftc == 'dq':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dq
            return d_trie_dq

        if ftc == 'dr':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dr
            return d_trie_dr

        if ftc == 'ds':
            from dbpedia_ent.dto.ent.n1.d import d_trie_ds
            return d_trie_ds

        if ftc == 'dt':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dt
            return d_trie_dt

        if ftc == 'du':
            from dbpedia_ent.dto.ent.n1.d import d_trie_du
            return d_trie_du

        if ftc == 'dv':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dv
            return d_trie_dv

        if ftc == 'dw':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dw
            return d_trie_dw

        if ftc == 'dx':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dx
            return d_trie_dx

        if ftc == 'dy':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dy
            return d_trie_dy

        if ftc == 'dz':
            from dbpedia_ent.dto.ent.n1.d import d_trie_dz
            return d_trie_dz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
