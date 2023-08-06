
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN3y(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'y_':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_y_
                    return d_trie_y_
        
                if ftc == 'ya':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_ya
                    return d_trie_ya
        
                if ftc == 'yb':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yb
                    return d_trie_yb
        
                if ftc == 'yc':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yc
                    return d_trie_yc
        
                if ftc == 'yd':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yd
                    return d_trie_yd
        
                if ftc == 'ye':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_ye
                    return d_trie_ye
        
                if ftc == 'yf':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yf
                    return d_trie_yf
        
                if ftc == 'yg':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yg
                    return d_trie_yg
        
                if ftc == 'yh':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yh
                    return d_trie_yh
        
                if ftc == 'yi':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yi
                    return d_trie_yi
        
                if ftc == 'yj':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yj
                    return d_trie_yj
        
                if ftc == 'yk':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yk
                    return d_trie_yk
        
                if ftc == 'yl':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yl
                    return d_trie_yl
        
                if ftc == 'ym':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_ym
                    return d_trie_ym
        
                if ftc == 'yn':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yn
                    return d_trie_yn
        
                if ftc == 'yo':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yo
                    return d_trie_yo
        
                if ftc == 'yp':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yp
                    return d_trie_yp
        
                if ftc == 'yq':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yq
                    return d_trie_yq
        
                if ftc == 'yr':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yr
                    return d_trie_yr
        
                if ftc == 'ys':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_ys
                    return d_trie_ys
        
                if ftc == 'yt':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yt
                    return d_trie_yt
        
                if ftc == 'yu':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yu
                    return d_trie_yu
        
                if ftc == 'yv':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yv
                    return d_trie_yv
        
                if ftc == 'yw':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yw
                    return d_trie_yw
        
                if ftc == 'yx':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yx
                    return d_trie_yx
        
                if ftc == 'yy':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yy
                    return d_trie_yy
        
                if ftc == 'yz':
                    from dbpedia_ent.dto.ent.n3.y import d_trie_yz
                    return d_trie_yz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        