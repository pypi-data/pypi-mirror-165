
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1v(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'va':
            from dbpedia_ent.dto.syn.n1.v import d_rev_va
            return d_rev_va
        
        if ftc == 'vb':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vb
            return d_rev_vb
        
        if ftc == 'vc':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vc
            return d_rev_vc
        
        if ftc == 'vd':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vd
            return d_rev_vd
        
        if ftc == 've':
            from dbpedia_ent.dto.syn.n1.v import d_rev_ve
            return d_rev_ve
        
        if ftc == 'vf':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vf
            return d_rev_vf
        
        if ftc == 'vg':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vg
            return d_rev_vg
        
        if ftc == 'vh':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vh
            return d_rev_vh
        
        if ftc == 'vi':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vi
            return d_rev_vi
        
        if ftc == 'vj':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vj
            return d_rev_vj
        
        if ftc == 'vk':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vk
            return d_rev_vk
        
        if ftc == 'vl':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vl
            return d_rev_vl
        
        if ftc == 'vm':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vm
            return d_rev_vm
        
        if ftc == 'vn':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vn
            return d_rev_vn
        
        if ftc == 'vo':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vo
            return d_rev_vo
        
        if ftc == 'vp':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vp
            return d_rev_vp
        
        if ftc == 'vq':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vq
            return d_rev_vq
        
        if ftc == 'vr':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vr
            return d_rev_vr
        
        if ftc == 'vs':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vs
            return d_rev_vs
        
        if ftc == 'vt':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vt
            return d_rev_vt
        
        if ftc == 'vu':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vu
            return d_rev_vu
        
        if ftc == 'vv':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vv
            return d_rev_vv
        
        if ftc == 'vw':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vw
            return d_rev_vw
        
        if ftc == 'vx':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vx
            return d_rev_vx
        
        if ftc == 'vy':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vy
            return d_rev_vy
        
        if ftc == 'vz':
            from dbpedia_ent.dto.syn.n1.v import d_rev_vz
            return d_rev_vz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        