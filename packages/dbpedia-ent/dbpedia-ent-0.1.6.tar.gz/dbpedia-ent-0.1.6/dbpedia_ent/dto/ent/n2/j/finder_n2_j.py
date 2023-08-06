
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN2j(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'j_':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_j_
                    return d_trie_j_
        
                if ftc == 'ja':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_ja
                    return d_trie_ja
        
                if ftc == 'jb':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jb
                    return d_trie_jb
        
                if ftc == 'jc':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jc
                    return d_trie_jc
        
                if ftc == 'jd':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jd
                    return d_trie_jd
        
                if ftc == 'je':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_je
                    return d_trie_je
        
                if ftc == 'jf':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jf
                    return d_trie_jf
        
                if ftc == 'jg':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jg
                    return d_trie_jg
        
                if ftc == 'jh':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jh
                    return d_trie_jh
        
                if ftc == 'ji':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_ji
                    return d_trie_ji
        
                if ftc == 'jj':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jj
                    return d_trie_jj
        
                if ftc == 'jk':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jk
                    return d_trie_jk
        
                if ftc == 'jl':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jl
                    return d_trie_jl
        
                if ftc == 'jm':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jm
                    return d_trie_jm
        
                if ftc == 'jn':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jn
                    return d_trie_jn
        
                if ftc == 'jo':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jo
                    return d_trie_jo
        
                if ftc == 'jp':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jp
                    return d_trie_jp
        
                if ftc == 'jq':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jq
                    return d_trie_jq
        
                if ftc == 'jr':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jr
                    return d_trie_jr
        
                if ftc == 'js':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_js
                    return d_trie_js
        
                if ftc == 'jt':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jt
                    return d_trie_jt
        
                if ftc == 'ju':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_ju
                    return d_trie_ju
        
                if ftc == 'jv':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jv
                    return d_trie_jv
        
                if ftc == 'jw':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jw
                    return d_trie_jw
        
                if ftc == 'jx':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jx
                    return d_trie_jx
        
                if ftc == 'jy':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jy
                    return d_trie_jy
        
                if ftc == 'jz':
                    from dbpedia_ent.dto.ent.n2.j import d_trie_jz
                    return d_trie_jz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        