
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN3p(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'pa':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pa
            return d_rev_pa
        
        if ftc == 'pb':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pb
            return d_rev_pb
        
        if ftc == 'pc':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pc
            return d_rev_pc
        
        if ftc == 'pd':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pd
            return d_rev_pd
        
        if ftc == 'pe':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pe
            return d_rev_pe
        
        if ftc == 'pf':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pf
            return d_rev_pf
        
        if ftc == 'pg':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pg
            return d_rev_pg
        
        if ftc == 'ph':
            from dbpedia_ent.dto.syn.n3.p import d_rev_ph
            return d_rev_ph
        
        if ftc == 'pi':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pi
            return d_rev_pi
        
        if ftc == 'pj':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pj
            return d_rev_pj
        
        if ftc == 'pk':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pk
            return d_rev_pk
        
        if ftc == 'pl':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pl
            return d_rev_pl
        
        if ftc == 'pm':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pm
            return d_rev_pm
        
        if ftc == 'pn':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pn
            return d_rev_pn
        
        if ftc == 'po':
            from dbpedia_ent.dto.syn.n3.p import d_rev_po
            return d_rev_po
        
        if ftc == 'pp':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pp
            return d_rev_pp
        
        if ftc == 'pq':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pq
            return d_rev_pq
        
        if ftc == 'pr':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pr
            return d_rev_pr
        
        if ftc == 'ps':
            from dbpedia_ent.dto.syn.n3.p import d_rev_ps
            return d_rev_ps
        
        if ftc == 'pt':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pt
            return d_rev_pt
        
        if ftc == 'pu':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pu
            return d_rev_pu
        
        if ftc == 'pv':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pv
            return d_rev_pv
        
        if ftc == 'pw':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pw
            return d_rev_pw
        
        if ftc == 'px':
            from dbpedia_ent.dto.syn.n3.p import d_rev_px
            return d_rev_px
        
        if ftc == 'py':
            from dbpedia_ent.dto.syn.n3.p import d_rev_py
            return d_rev_py
        
        if ftc == 'pz':
            from dbpedia_ent.dto.syn.n3.p import d_rev_pz
            return d_rev_pz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        