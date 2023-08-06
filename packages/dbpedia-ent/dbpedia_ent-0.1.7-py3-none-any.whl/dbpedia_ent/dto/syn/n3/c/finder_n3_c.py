
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN3c(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ca':
            from dbpedia_ent.dto.syn.n3.c import d_rev_ca
            return d_rev_ca
        
        if ftc == 'cb':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cb
            return d_rev_cb
        
        if ftc == 'cc':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cc
            return d_rev_cc
        
        if ftc == 'cd':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cd
            return d_rev_cd
        
        if ftc == 'ce':
            from dbpedia_ent.dto.syn.n3.c import d_rev_ce
            return d_rev_ce
        
        if ftc == 'cf':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cf
            return d_rev_cf
        
        if ftc == 'cg':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cg
            return d_rev_cg
        
        if ftc == 'ch':
            from dbpedia_ent.dto.syn.n3.c import d_rev_ch
            return d_rev_ch
        
        if ftc == 'ci':
            from dbpedia_ent.dto.syn.n3.c import d_rev_ci
            return d_rev_ci
        
        if ftc == 'cj':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cj
            return d_rev_cj
        
        if ftc == 'ck':
            from dbpedia_ent.dto.syn.n3.c import d_rev_ck
            return d_rev_ck
        
        if ftc == 'cl':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cl
            return d_rev_cl
        
        if ftc == 'cm':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cm
            return d_rev_cm
        
        if ftc == 'cn':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cn
            return d_rev_cn
        
        if ftc == 'co':
            from dbpedia_ent.dto.syn.n3.c import d_rev_co
            return d_rev_co
        
        if ftc == 'cp':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cp
            return d_rev_cp
        
        if ftc == 'cq':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cq
            return d_rev_cq
        
        if ftc == 'cr':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cr
            return d_rev_cr
        
        if ftc == 'cs':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cs
            return d_rev_cs
        
        if ftc == 'ct':
            from dbpedia_ent.dto.syn.n3.c import d_rev_ct
            return d_rev_ct
        
        if ftc == 'cu':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cu
            return d_rev_cu
        
        if ftc == 'cv':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cv
            return d_rev_cv
        
        if ftc == 'cw':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cw
            return d_rev_cw
        
        if ftc == 'cx':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cx
            return d_rev_cx
        
        if ftc == 'cy':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cy
            return d_rev_cy
        
        if ftc == 'cz':
            from dbpedia_ent.dto.syn.n3.c import d_rev_cz
            return d_rev_cz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        