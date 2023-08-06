
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1m(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ma':
            from dbpedia_ent.dto.syn.n1.m import d_rev_ma
            return d_rev_ma
        
        if ftc == 'mb':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mb
            return d_rev_mb
        
        if ftc == 'mc':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mc
            return d_rev_mc
        
        if ftc == 'md':
            from dbpedia_ent.dto.syn.n1.m import d_rev_md
            return d_rev_md
        
        if ftc == 'me':
            from dbpedia_ent.dto.syn.n1.m import d_rev_me
            return d_rev_me
        
        if ftc == 'mf':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mf
            return d_rev_mf
        
        if ftc == 'mg':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mg
            return d_rev_mg
        
        if ftc == 'mh':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mh
            return d_rev_mh
        
        if ftc == 'mi':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mi
            return d_rev_mi
        
        if ftc == 'mj':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mj
            return d_rev_mj
        
        if ftc == 'mk':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mk
            return d_rev_mk
        
        if ftc == 'ml':
            from dbpedia_ent.dto.syn.n1.m import d_rev_ml
            return d_rev_ml
        
        if ftc == 'mm':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mm
            return d_rev_mm
        
        if ftc == 'mn':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mn
            return d_rev_mn
        
        if ftc == 'mo':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mo
            return d_rev_mo
        
        if ftc == 'mp':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mp
            return d_rev_mp
        
        if ftc == 'mq':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mq
            return d_rev_mq
        
        if ftc == 'mr':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mr
            return d_rev_mr
        
        if ftc == 'ms':
            from dbpedia_ent.dto.syn.n1.m import d_rev_ms
            return d_rev_ms
        
        if ftc == 'mt':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mt
            return d_rev_mt
        
        if ftc == 'mu':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mu
            return d_rev_mu
        
        if ftc == 'mv':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mv
            return d_rev_mv
        
        if ftc == 'mw':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mw
            return d_rev_mw
        
        if ftc == 'mx':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mx
            return d_rev_mx
        
        if ftc == 'my':
            from dbpedia_ent.dto.syn.n1.m import d_rev_my
            return d_rev_my
        
        if ftc == 'mz':
            from dbpedia_ent.dto.syn.n1.m import d_rev_mz
            return d_rev_mz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        