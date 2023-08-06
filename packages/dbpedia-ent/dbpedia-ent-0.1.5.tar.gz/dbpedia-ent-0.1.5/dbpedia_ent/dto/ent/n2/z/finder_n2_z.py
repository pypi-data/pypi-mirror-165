
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN2z(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'z_':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_z_
                    return d_trie_z_
        
                if ftc == 'za':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_za
                    return d_trie_za
        
                if ftc == 'zb':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zb
                    return d_trie_zb
        
                if ftc == 'zc':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zc
                    return d_trie_zc
        
                if ftc == 'zd':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zd
                    return d_trie_zd
        
                if ftc == 'ze':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_ze
                    return d_trie_ze
        
                if ftc == 'zf':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zf
                    return d_trie_zf
        
                if ftc == 'zg':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zg
                    return d_trie_zg
        
                if ftc == 'zh':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zh
                    return d_trie_zh
        
                if ftc == 'zi':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zi
                    return d_trie_zi
        
                if ftc == 'zj':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zj
                    return d_trie_zj
        
                if ftc == 'zk':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zk
                    return d_trie_zk
        
                if ftc == 'zl':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zl
                    return d_trie_zl
        
                if ftc == 'zm':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zm
                    return d_trie_zm
        
                if ftc == 'zn':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zn
                    return d_trie_zn
        
                if ftc == 'zo':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zo
                    return d_trie_zo
        
                if ftc == 'zp':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zp
                    return d_trie_zp
        
                if ftc == 'zq':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zq
                    return d_trie_zq
        
                if ftc == 'zr':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zr
                    return d_trie_zr
        
                if ftc == 'zs':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zs
                    return d_trie_zs
        
                if ftc == 'zt':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zt
                    return d_trie_zt
        
                if ftc == 'zu':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zu
                    return d_trie_zu
        
                if ftc == 'zv':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zv
                    return d_trie_zv
        
                if ftc == 'zw':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zw
                    return d_trie_zw
        
                if ftc == 'zx':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zx
                    return d_trie_zx
        
                if ftc == 'zy':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zy
                    return d_trie_zy
        
                if ftc == 'zz':
                    from dbpedia_ent.dto.ent.n2.z import d_trie_zz
                    return d_trie_zz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        