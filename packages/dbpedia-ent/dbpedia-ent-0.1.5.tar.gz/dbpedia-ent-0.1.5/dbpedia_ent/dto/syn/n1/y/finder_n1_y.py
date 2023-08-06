
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1y(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ya':
            from dbpedia_ent.dto.syn.n1.y import d_rev_ya
            return d_rev_ya
        
        if ftc == 'yb':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yb
            return d_rev_yb
        
        if ftc == 'yc':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yc
            return d_rev_yc
        
        if ftc == 'yd':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yd
            return d_rev_yd
        
        if ftc == 'ye':
            from dbpedia_ent.dto.syn.n1.y import d_rev_ye
            return d_rev_ye
        
        if ftc == 'yf':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yf
            return d_rev_yf
        
        if ftc == 'yg':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yg
            return d_rev_yg
        
        if ftc == 'yh':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yh
            return d_rev_yh
        
        if ftc == 'yi':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yi
            return d_rev_yi
        
        if ftc == 'yj':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yj
            return d_rev_yj
        
        if ftc == 'yk':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yk
            return d_rev_yk
        
        if ftc == 'yl':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yl
            return d_rev_yl
        
        if ftc == 'ym':
            from dbpedia_ent.dto.syn.n1.y import d_rev_ym
            return d_rev_ym
        
        if ftc == 'yn':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yn
            return d_rev_yn
        
        if ftc == 'yo':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yo
            return d_rev_yo
        
        if ftc == 'yp':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yp
            return d_rev_yp
        
        if ftc == 'yq':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yq
            return d_rev_yq
        
        if ftc == 'yr':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yr
            return d_rev_yr
        
        if ftc == 'ys':
            from dbpedia_ent.dto.syn.n1.y import d_rev_ys
            return d_rev_ys
        
        if ftc == 'yt':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yt
            return d_rev_yt
        
        if ftc == 'yu':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yu
            return d_rev_yu
        
        if ftc == 'yv':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yv
            return d_rev_yv
        
        if ftc == 'yw':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yw
            return d_rev_yw
        
        if ftc == 'yx':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yx
            return d_rev_yx
        
        if ftc == 'yy':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yy
            return d_rev_yy
        
        if ftc == 'yz':
            from dbpedia_ent.dto.syn.n1.y import d_rev_yz
            return d_rev_yz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        