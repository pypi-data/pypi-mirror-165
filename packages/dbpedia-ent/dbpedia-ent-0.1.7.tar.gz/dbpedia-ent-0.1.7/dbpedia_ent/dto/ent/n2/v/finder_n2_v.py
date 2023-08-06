
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN2v(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'v_':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_v_
                    return d_trie_v_
        
                if ftc == 'va':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_va
                    return d_trie_va
        
                if ftc == 'vb':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vb
                    return d_trie_vb
        
                if ftc == 'vc':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vc
                    return d_trie_vc
        
                if ftc == 'vd':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vd
                    return d_trie_vd
        
                if ftc == 've':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_ve
                    return d_trie_ve
        
                if ftc == 'vf':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vf
                    return d_trie_vf
        
                if ftc == 'vg':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vg
                    return d_trie_vg
        
                if ftc == 'vh':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vh
                    return d_trie_vh
        
                if ftc == 'vi':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vi
                    return d_trie_vi
        
                if ftc == 'vj':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vj
                    return d_trie_vj
        
                if ftc == 'vk':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vk
                    return d_trie_vk
        
                if ftc == 'vl':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vl
                    return d_trie_vl
        
                if ftc == 'vm':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vm
                    return d_trie_vm
        
                if ftc == 'vn':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vn
                    return d_trie_vn
        
                if ftc == 'vo':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vo
                    return d_trie_vo
        
                if ftc == 'vp':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vp
                    return d_trie_vp
        
                if ftc == 'vq':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vq
                    return d_trie_vq
        
                if ftc == 'vr':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vr
                    return d_trie_vr
        
                if ftc == 'vs':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vs
                    return d_trie_vs
        
                if ftc == 'vt':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vt
                    return d_trie_vt
        
                if ftc == 'vu':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vu
                    return d_trie_vu
        
                if ftc == 'vv':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vv
                    return d_trie_vv
        
                if ftc == 'vw':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vw
                    return d_trie_vw
        
                if ftc == 'vx':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vx
                    return d_trie_vx
        
                if ftc == 'vy':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vy
                    return d_trie_vy
        
                if ftc == 'vz':
                    from dbpedia_ent.dto.ent.n2.v import d_trie_vz
                    return d_trie_vz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        