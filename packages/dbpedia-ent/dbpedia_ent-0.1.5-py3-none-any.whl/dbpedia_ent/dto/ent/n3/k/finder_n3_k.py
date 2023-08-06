
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN3k(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'k_':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_k_
                    return d_trie_k_
        
                if ftc == 'ka':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_ka
                    return d_trie_ka
        
                if ftc == 'kb':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kb
                    return d_trie_kb
        
                if ftc == 'kc':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kc
                    return d_trie_kc
        
                if ftc == 'kd':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kd
                    return d_trie_kd
        
                if ftc == 'ke':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_ke
                    return d_trie_ke
        
                if ftc == 'kf':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kf
                    return d_trie_kf
        
                if ftc == 'kg':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kg
                    return d_trie_kg
        
                if ftc == 'kh':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kh
                    return d_trie_kh
        
                if ftc == 'ki':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_ki
                    return d_trie_ki
        
                if ftc == 'kj':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kj
                    return d_trie_kj
        
                if ftc == 'kk':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kk
                    return d_trie_kk
        
                if ftc == 'kl':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kl
                    return d_trie_kl
        
                if ftc == 'km':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_km
                    return d_trie_km
        
                if ftc == 'kn':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kn
                    return d_trie_kn
        
                if ftc == 'ko':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_ko
                    return d_trie_ko
        
                if ftc == 'kp':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kp
                    return d_trie_kp
        
                if ftc == 'kq':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kq
                    return d_trie_kq
        
                if ftc == 'kr':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kr
                    return d_trie_kr
        
                if ftc == 'ks':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_ks
                    return d_trie_ks
        
                if ftc == 'kt':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kt
                    return d_trie_kt
        
                if ftc == 'ku':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_ku
                    return d_trie_ku
        
                if ftc == 'kv':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kv
                    return d_trie_kv
        
                if ftc == 'kw':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kw
                    return d_trie_kw
        
                if ftc == 'kx':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kx
                    return d_trie_kx
        
                if ftc == 'ky':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_ky
                    return d_trie_ky
        
                if ftc == 'kz':
                    from dbpedia_ent.dto.ent.n3.k import d_trie_kz
                    return d_trie_kz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        