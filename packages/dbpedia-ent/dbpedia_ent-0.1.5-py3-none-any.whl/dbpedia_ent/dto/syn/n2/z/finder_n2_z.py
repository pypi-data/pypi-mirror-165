
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN2z(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'za':
            from dbpedia_ent.dto.syn.n2.z import d_rev_za
            return d_rev_za
        
        if ftc == 'zb':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zb
            return d_rev_zb
        
        if ftc == 'zc':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zc
            return d_rev_zc
        
        if ftc == 'zd':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zd
            return d_rev_zd
        
        if ftc == 'ze':
            from dbpedia_ent.dto.syn.n2.z import d_rev_ze
            return d_rev_ze
        
        if ftc == 'zf':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zf
            return d_rev_zf
        
        if ftc == 'zg':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zg
            return d_rev_zg
        
        if ftc == 'zh':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zh
            return d_rev_zh
        
        if ftc == 'zi':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zi
            return d_rev_zi
        
        if ftc == 'zj':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zj
            return d_rev_zj
        
        if ftc == 'zk':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zk
            return d_rev_zk
        
        if ftc == 'zl':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zl
            return d_rev_zl
        
        if ftc == 'zm':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zm
            return d_rev_zm
        
        if ftc == 'zn':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zn
            return d_rev_zn
        
        if ftc == 'zo':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zo
            return d_rev_zo
        
        if ftc == 'zp':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zp
            return d_rev_zp
        
        if ftc == 'zq':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zq
            return d_rev_zq
        
        if ftc == 'zr':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zr
            return d_rev_zr
        
        if ftc == 'zs':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zs
            return d_rev_zs
        
        if ftc == 'zt':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zt
            return d_rev_zt
        
        if ftc == 'zu':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zu
            return d_rev_zu
        
        if ftc == 'zv':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zv
            return d_rev_zv
        
        if ftc == 'zw':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zw
            return d_rev_zw
        
        if ftc == 'zx':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zx
            return d_rev_zx
        
        if ftc == 'zy':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zy
            return d_rev_zy
        
        if ftc == 'zz':
            from dbpedia_ent.dto.syn.n2.z import d_rev_zz
            return d_rev_zz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        