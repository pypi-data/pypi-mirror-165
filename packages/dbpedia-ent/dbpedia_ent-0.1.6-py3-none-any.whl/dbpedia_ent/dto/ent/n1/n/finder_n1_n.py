
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1n(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'n_':
            from dbpedia_ent.dto.ent.n1.n import d_trie_n_
            return d_trie_n_

        if ftc == 'na':
            from dbpedia_ent.dto.ent.n1.n import d_trie_na
            return d_trie_na

        if ftc == 'nb':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nb
            return d_trie_nb

        if ftc == 'nc':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nc
            return d_trie_nc

        if ftc == 'nd':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nd
            return d_trie_nd

        if ftc == 'ne':
            from dbpedia_ent.dto.ent.n1.n import d_trie_ne
            return d_trie_ne

        if ftc == 'nf':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nf
            return d_trie_nf

        if ftc == 'ng':
            from dbpedia_ent.dto.ent.n1.n import d_trie_ng
            return d_trie_ng

        if ftc == 'nh':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nh
            return d_trie_nh

        if ftc == 'ni':
            from dbpedia_ent.dto.ent.n1.n import d_trie_ni
            return d_trie_ni

        if ftc == 'nj':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nj
            return d_trie_nj

        if ftc == 'nk':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nk
            return d_trie_nk

        if ftc == 'nl':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nl
            return d_trie_nl

        if ftc == 'nm':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nm
            return d_trie_nm

        if ftc == 'nn':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nn
            return d_trie_nn

        if ftc == 'no':
            from dbpedia_ent.dto.ent.n1.n import d_trie_no
            return d_trie_no

        if ftc == 'np':
            from dbpedia_ent.dto.ent.n1.n import d_trie_np
            return d_trie_np

        if ftc == 'nq':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nq
            return d_trie_nq

        if ftc == 'nr':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nr
            return d_trie_nr

        if ftc == 'ns':
            from dbpedia_ent.dto.ent.n1.n import d_trie_ns
            return d_trie_ns

        if ftc == 'nt':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nt
            return d_trie_nt

        if ftc == 'nu':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nu
            return d_trie_nu

        if ftc == 'nv':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nv
            return d_trie_nv

        if ftc == 'nw':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nw
            return d_trie_nw

        if ftc == 'nx':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nx
            return d_trie_nx

        if ftc == 'ny':
            from dbpedia_ent.dto.ent.n1.n import d_trie_ny
            return d_trie_ny

        if ftc == 'nz':
            from dbpedia_ent.dto.ent.n1.n import d_trie_nz
            return d_trie_nz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
