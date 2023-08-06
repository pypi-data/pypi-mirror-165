
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN3r(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ra':
            from dbpedia_ent.dto.syn.n3.r import d_rev_ra
            return d_rev_ra
        
        if ftc == 'rb':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rb
            return d_rev_rb
        
        if ftc == 'rc':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rc
            return d_rev_rc
        
        if ftc == 'rd':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rd
            return d_rev_rd
        
        if ftc == 're':
            from dbpedia_ent.dto.syn.n3.r import d_rev_re
            return d_rev_re
        
        if ftc == 'rf':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rf
            return d_rev_rf
        
        if ftc == 'rg':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rg
            return d_rev_rg
        
        if ftc == 'rh':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rh
            return d_rev_rh
        
        if ftc == 'ri':
            from dbpedia_ent.dto.syn.n3.r import d_rev_ri
            return d_rev_ri
        
        if ftc == 'rj':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rj
            return d_rev_rj
        
        if ftc == 'rk':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rk
            return d_rev_rk
        
        if ftc == 'rl':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rl
            return d_rev_rl
        
        if ftc == 'rm':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rm
            return d_rev_rm
        
        if ftc == 'rn':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rn
            return d_rev_rn
        
        if ftc == 'ro':
            from dbpedia_ent.dto.syn.n3.r import d_rev_ro
            return d_rev_ro
        
        if ftc == 'rp':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rp
            return d_rev_rp
        
        if ftc == 'rq':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rq
            return d_rev_rq
        
        if ftc == 'rr':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rr
            return d_rev_rr
        
        if ftc == 'rs':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rs
            return d_rev_rs
        
        if ftc == 'rt':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rt
            return d_rev_rt
        
        if ftc == 'ru':
            from dbpedia_ent.dto.syn.n3.r import d_rev_ru
            return d_rev_ru
        
        if ftc == 'rv':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rv
            return d_rev_rv
        
        if ftc == 'rw':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rw
            return d_rev_rw
        
        if ftc == 'rx':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rx
            return d_rev_rx
        
        if ftc == 'ry':
            from dbpedia_ent.dto.syn.n3.r import d_rev_ry
            return d_rev_ry
        
        if ftc == 'rz':
            from dbpedia_ent.dto.syn.n3.r import d_rev_rz
            return d_rev_rz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        