
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN3j(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ja':
            from dbpedia_ent.dto.syn.n3.j import d_rev_ja
            return d_rev_ja
        
        if ftc == 'jb':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jb
            return d_rev_jb
        
        if ftc == 'jc':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jc
            return d_rev_jc
        
        if ftc == 'jd':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jd
            return d_rev_jd
        
        if ftc == 'je':
            from dbpedia_ent.dto.syn.n3.j import d_rev_je
            return d_rev_je
        
        if ftc == 'jf':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jf
            return d_rev_jf
        
        if ftc == 'jg':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jg
            return d_rev_jg
        
        if ftc == 'jh':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jh
            return d_rev_jh
        
        if ftc == 'ji':
            from dbpedia_ent.dto.syn.n3.j import d_rev_ji
            return d_rev_ji
        
        if ftc == 'jj':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jj
            return d_rev_jj
        
        if ftc == 'jk':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jk
            return d_rev_jk
        
        if ftc == 'jl':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jl
            return d_rev_jl
        
        if ftc == 'jm':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jm
            return d_rev_jm
        
        if ftc == 'jn':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jn
            return d_rev_jn
        
        if ftc == 'jo':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jo
            return d_rev_jo
        
        if ftc == 'jp':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jp
            return d_rev_jp
        
        if ftc == 'jq':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jq
            return d_rev_jq
        
        if ftc == 'jr':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jr
            return d_rev_jr
        
        if ftc == 'js':
            from dbpedia_ent.dto.syn.n3.j import d_rev_js
            return d_rev_js
        
        if ftc == 'jt':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jt
            return d_rev_jt
        
        if ftc == 'ju':
            from dbpedia_ent.dto.syn.n3.j import d_rev_ju
            return d_rev_ju
        
        if ftc == 'jv':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jv
            return d_rev_jv
        
        if ftc == 'jw':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jw
            return d_rev_jw
        
        if ftc == 'jx':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jx
            return d_rev_jx
        
        if ftc == 'jy':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jy
            return d_rev_jy
        
        if ftc == 'jz':
            from dbpedia_ent.dto.syn.n3.j import d_rev_jz
            return d_rev_jz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        