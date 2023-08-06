
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1n(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'na':
            from dbpedia_ent.dto.syn.n1.n import d_rev_na
            return d_rev_na
        
        if ftc == 'nb':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nb
            return d_rev_nb
        
        if ftc == 'nc':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nc
            return d_rev_nc
        
        if ftc == 'nd':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nd
            return d_rev_nd
        
        if ftc == 'ne':
            from dbpedia_ent.dto.syn.n1.n import d_rev_ne
            return d_rev_ne
        
        if ftc == 'nf':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nf
            return d_rev_nf
        
        if ftc == 'ng':
            from dbpedia_ent.dto.syn.n1.n import d_rev_ng
            return d_rev_ng
        
        if ftc == 'nh':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nh
            return d_rev_nh
        
        if ftc == 'ni':
            from dbpedia_ent.dto.syn.n1.n import d_rev_ni
            return d_rev_ni
        
        if ftc == 'nj':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nj
            return d_rev_nj
        
        if ftc == 'nk':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nk
            return d_rev_nk
        
        if ftc == 'nl':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nl
            return d_rev_nl
        
        if ftc == 'nm':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nm
            return d_rev_nm
        
        if ftc == 'nn':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nn
            return d_rev_nn
        
        if ftc == 'no':
            from dbpedia_ent.dto.syn.n1.n import d_rev_no
            return d_rev_no
        
        if ftc == 'np':
            from dbpedia_ent.dto.syn.n1.n import d_rev_np
            return d_rev_np
        
        if ftc == 'nq':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nq
            return d_rev_nq
        
        if ftc == 'nr':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nr
            return d_rev_nr
        
        if ftc == 'ns':
            from dbpedia_ent.dto.syn.n1.n import d_rev_ns
            return d_rev_ns
        
        if ftc == 'nt':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nt
            return d_rev_nt
        
        if ftc == 'nu':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nu
            return d_rev_nu
        
        if ftc == 'nv':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nv
            return d_rev_nv
        
        if ftc == 'nw':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nw
            return d_rev_nw
        
        if ftc == 'nx':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nx
            return d_rev_nx
        
        if ftc == 'ny':
            from dbpedia_ent.dto.syn.n1.n import d_rev_ny
            return d_rev_ny
        
        if ftc == 'nz':
            from dbpedia_ent.dto.syn.n1.n import d_rev_nz
            return d_rev_nz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        