
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN3w(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'wa':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wa
            return d_rev_wa
        
        if ftc == 'wb':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wb
            return d_rev_wb
        
        if ftc == 'wc':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wc
            return d_rev_wc
        
        if ftc == 'wd':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wd
            return d_rev_wd
        
        if ftc == 'we':
            from dbpedia_ent.dto.syn.n3.w import d_rev_we
            return d_rev_we
        
        if ftc == 'wf':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wf
            return d_rev_wf
        
        if ftc == 'wg':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wg
            return d_rev_wg
        
        if ftc == 'wh':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wh
            return d_rev_wh
        
        if ftc == 'wi':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wi
            return d_rev_wi
        
        if ftc == 'wj':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wj
            return d_rev_wj
        
        if ftc == 'wk':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wk
            return d_rev_wk
        
        if ftc == 'wl':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wl
            return d_rev_wl
        
        if ftc == 'wm':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wm
            return d_rev_wm
        
        if ftc == 'wn':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wn
            return d_rev_wn
        
        if ftc == 'wo':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wo
            return d_rev_wo
        
        if ftc == 'wp':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wp
            return d_rev_wp
        
        if ftc == 'wq':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wq
            return d_rev_wq
        
        if ftc == 'wr':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wr
            return d_rev_wr
        
        if ftc == 'ws':
            from dbpedia_ent.dto.syn.n3.w import d_rev_ws
            return d_rev_ws
        
        if ftc == 'wt':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wt
            return d_rev_wt
        
        if ftc == 'wu':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wu
            return d_rev_wu
        
        if ftc == 'wv':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wv
            return d_rev_wv
        
        if ftc == 'ww':
            from dbpedia_ent.dto.syn.n3.w import d_rev_ww
            return d_rev_ww
        
        if ftc == 'wx':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wx
            return d_rev_wx
        
        if ftc == 'wy':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wy
            return d_rev_wy
        
        if ftc == 'wz':
            from dbpedia_ent.dto.syn.n3.w import d_rev_wz
            return d_rev_wz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        