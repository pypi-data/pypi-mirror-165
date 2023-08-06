
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN2d(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'da':
            from dbpedia_ent.dto.syn.n2.d import d_rev_da
            return d_rev_da
        
        if ftc == 'db':
            from dbpedia_ent.dto.syn.n2.d import d_rev_db
            return d_rev_db
        
        if ftc == 'dc':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dc
            return d_rev_dc
        
        if ftc == 'dd':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dd
            return d_rev_dd
        
        if ftc == 'de':
            from dbpedia_ent.dto.syn.n2.d import d_rev_de
            return d_rev_de
        
        if ftc == 'df':
            from dbpedia_ent.dto.syn.n2.d import d_rev_df
            return d_rev_df
        
        if ftc == 'dg':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dg
            return d_rev_dg
        
        if ftc == 'dh':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dh
            return d_rev_dh
        
        if ftc == 'di':
            from dbpedia_ent.dto.syn.n2.d import d_rev_di
            return d_rev_di
        
        if ftc == 'dj':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dj
            return d_rev_dj
        
        if ftc == 'dk':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dk
            return d_rev_dk
        
        if ftc == 'dl':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dl
            return d_rev_dl
        
        if ftc == 'dm':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dm
            return d_rev_dm
        
        if ftc == 'dn':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dn
            return d_rev_dn
        
        if ftc == 'do':
            from dbpedia_ent.dto.syn.n2.d import d_rev_do
            return d_rev_do
        
        if ftc == 'dp':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dp
            return d_rev_dp
        
        if ftc == 'dq':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dq
            return d_rev_dq
        
        if ftc == 'dr':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dr
            return d_rev_dr
        
        if ftc == 'ds':
            from dbpedia_ent.dto.syn.n2.d import d_rev_ds
            return d_rev_ds
        
        if ftc == 'dt':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dt
            return d_rev_dt
        
        if ftc == 'du':
            from dbpedia_ent.dto.syn.n2.d import d_rev_du
            return d_rev_du
        
        if ftc == 'dv':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dv
            return d_rev_dv
        
        if ftc == 'dw':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dw
            return d_rev_dw
        
        if ftc == 'dx':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dx
            return d_rev_dx
        
        if ftc == 'dy':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dy
            return d_rev_dy
        
        if ftc == 'dz':
            from dbpedia_ent.dto.syn.n2.d import d_rev_dz
            return d_rev_dz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        