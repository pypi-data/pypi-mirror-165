
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN3w(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'w_':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_w_
                    return d_trie_w_
        
                if ftc == 'wa':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wa
                    return d_trie_wa
        
                if ftc == 'wb':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wb
                    return d_trie_wb
        
                if ftc == 'wc':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wc
                    return d_trie_wc
        
                if ftc == 'wd':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wd
                    return d_trie_wd
        
                if ftc == 'we':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_we
                    return d_trie_we
        
                if ftc == 'wf':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wf
                    return d_trie_wf
        
                if ftc == 'wg':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wg
                    return d_trie_wg
        
                if ftc == 'wh':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wh
                    return d_trie_wh
        
                if ftc == 'wi':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wi
                    return d_trie_wi
        
                if ftc == 'wj':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wj
                    return d_trie_wj
        
                if ftc == 'wk':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wk
                    return d_trie_wk
        
                if ftc == 'wl':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wl
                    return d_trie_wl
        
                if ftc == 'wm':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wm
                    return d_trie_wm
        
                if ftc == 'wn':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wn
                    return d_trie_wn
        
                if ftc == 'wo':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wo
                    return d_trie_wo
        
                if ftc == 'wp':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wp
                    return d_trie_wp
        
                # if ftc == 'wq':
                #     from dbpedia_ent.dto.ent.n3.w import d_trie_wq
                #     return d_trie_wq
        
                if ftc == 'wr':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wr
                    return d_trie_wr
        
                if ftc == 'ws':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_ws
                    return d_trie_ws
        
                if ftc == 'wt':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wt
                    return d_trie_wt
        
                if ftc == 'wu':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wu
                    return d_trie_wu
        
                if ftc == 'wv':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wv
                    return d_trie_wv
        
                if ftc == 'ww':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_ww
                    return d_trie_ww
        
                if ftc == 'wx':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wx
                    return d_trie_wx
        
                if ftc == 'wy':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wy
                    return d_trie_wy
        
                if ftc == 'wz':
                    from dbpedia_ent.dto.ent.n3.w import d_trie_wz
                    return d_trie_wz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        