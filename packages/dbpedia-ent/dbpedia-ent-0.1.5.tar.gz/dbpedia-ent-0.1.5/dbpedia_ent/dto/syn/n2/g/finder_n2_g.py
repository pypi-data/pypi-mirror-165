
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN2g(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ga':
            from dbpedia_ent.dto.syn.n2.g import d_rev_ga
            return d_rev_ga
        
        if ftc == 'gb':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gb
            return d_rev_gb
        
        if ftc == 'gc':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gc
            return d_rev_gc
        
        if ftc == 'gd':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gd
            return d_rev_gd
        
        if ftc == 'ge':
            from dbpedia_ent.dto.syn.n2.g import d_rev_ge
            return d_rev_ge
        
        if ftc == 'gf':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gf
            return d_rev_gf
        
        if ftc == 'gg':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gg
            return d_rev_gg
        
        if ftc == 'gh':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gh
            return d_rev_gh
        
        if ftc == 'gi':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gi
            return d_rev_gi
        
        if ftc == 'gj':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gj
            return d_rev_gj
        
        if ftc == 'gk':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gk
            return d_rev_gk
        
        if ftc == 'gl':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gl
            return d_rev_gl
        
        if ftc == 'gm':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gm
            return d_rev_gm
        
        if ftc == 'gn':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gn
            return d_rev_gn
        
        if ftc == 'go':
            from dbpedia_ent.dto.syn.n2.g import d_rev_go
            return d_rev_go
        
        if ftc == 'gp':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gp
            return d_rev_gp
        
        if ftc == 'gq':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gq
            return d_rev_gq
        
        if ftc == 'gr':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gr
            return d_rev_gr
        
        if ftc == 'gs':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gs
            return d_rev_gs
        
        if ftc == 'gt':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gt
            return d_rev_gt
        
        if ftc == 'gu':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gu
            return d_rev_gu
        
        if ftc == 'gv':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gv
            return d_rev_gv
        
        if ftc == 'gw':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gw
            return d_rev_gw
        
        if ftc == 'gx':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gx
            return d_rev_gx
        
        if ftc == 'gy':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gy
            return d_rev_gy
        
        if ftc == 'gz':
            from dbpedia_ent.dto.syn.n2.g import d_rev_gz
            return d_rev_gz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        