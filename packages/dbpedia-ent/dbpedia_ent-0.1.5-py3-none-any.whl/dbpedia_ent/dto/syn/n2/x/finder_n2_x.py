
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN2x(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'xa':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xa
            return d_rev_xa
        
        if ftc == 'xb':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xb
            return d_rev_xb
        
        if ftc == 'xc':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xc
            return d_rev_xc
        
        if ftc == 'xd':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xd
            return d_rev_xd
        
        if ftc == 'xe':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xe
            return d_rev_xe
        
        if ftc == 'xf':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xf
            return d_rev_xf
        
        if ftc == 'xg':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xg
            return d_rev_xg
        
        if ftc == 'xh':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xh
            return d_rev_xh
        
        if ftc == 'xi':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xi
            return d_rev_xi
        
        if ftc == 'xj':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xj
            return d_rev_xj
        
        if ftc == 'xk':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xk
            return d_rev_xk
        
        if ftc == 'xl':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xl
            return d_rev_xl
        
        if ftc == 'xm':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xm
            return d_rev_xm
        
        if ftc == 'xn':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xn
            return d_rev_xn
        
        if ftc == 'xo':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xo
            return d_rev_xo
        
        if ftc == 'xp':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xp
            return d_rev_xp
        
        if ftc == 'xq':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xq
            return d_rev_xq
        
        if ftc == 'xr':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xr
            return d_rev_xr
        
        if ftc == 'xs':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xs
            return d_rev_xs
        
        if ftc == 'xt':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xt
            return d_rev_xt
        
        if ftc == 'xu':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xu
            return d_rev_xu
        
        if ftc == 'xv':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xv
            return d_rev_xv
        
        if ftc == 'xw':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xw
            return d_rev_xw
        
        if ftc == 'xx':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xx
            return d_rev_xx
        
        if ftc == 'xy':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xy
            return d_rev_xy
        
        if ftc == 'xz':
            from dbpedia_ent.dto.syn.n2.x import d_rev_xz
            return d_rev_xz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        