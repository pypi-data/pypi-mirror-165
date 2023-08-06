
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN3x(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'x_':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_x_
                    return d_trie_x_
        
                if ftc == 'xa':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xa
                    return d_trie_xa
        
                if ftc == 'xb':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xb
                    return d_trie_xb
        
                if ftc == 'xc':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xc
                    return d_trie_xc
        
                if ftc == 'xd':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xd
                    return d_trie_xd
        
                if ftc == 'xe':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xe
                    return d_trie_xe
        
                if ftc == 'xf':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xf
                    return d_trie_xf
        
                if ftc == 'xg':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xg
                    return d_trie_xg
        
                if ftc == 'xh':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xh
                    return d_trie_xh
        
                if ftc == 'xi':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xi
                    return d_trie_xi
        
                if ftc == 'xj':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xj
                    return d_trie_xj
        
                if ftc == 'xk':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xk
                    return d_trie_xk
        
                if ftc == 'xl':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xl
                    return d_trie_xl
        
                if ftc == 'xm':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xm
                    return d_trie_xm
        
                if ftc == 'xn':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xn
                    return d_trie_xn
        
                if ftc == 'xo':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xo
                    return d_trie_xo
        
                if ftc == 'xp':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xp
                    return d_trie_xp
        
                if ftc == 'xq':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xq
                    return d_trie_xq
        
                if ftc == 'xr':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xr
                    return d_trie_xr
        
                if ftc == 'xs':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xs
                    return d_trie_xs
        
                if ftc == 'xt':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xt
                    return d_trie_xt
        
                if ftc == 'xu':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xu
                    return d_trie_xu
        
                if ftc == 'xv':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xv
                    return d_trie_xv
        
                if ftc == 'xw':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xw
                    return d_trie_xw
        
                if ftc == 'xx':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xx
                    return d_trie_xx
        
                if ftc == 'xy':
                    from dbpedia_ent.dto.ent.n3.x import d_trie_xy
                    return d_trie_xy
        
                # if ftc == 'xz':
                #     from dbpedia_ent.dto.ent.n3.x import d_trie_xz
                #     return d_trie_xz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        