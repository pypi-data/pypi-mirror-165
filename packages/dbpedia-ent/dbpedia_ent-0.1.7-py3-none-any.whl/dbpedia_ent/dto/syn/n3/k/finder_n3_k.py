
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN3k(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ka':
            from dbpedia_ent.dto.syn.n3.k import d_rev_ka
            return d_rev_ka
        
        if ftc == 'kb':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kb
            return d_rev_kb
        
        if ftc == 'kc':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kc
            return d_rev_kc
        
        if ftc == 'kd':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kd
            return d_rev_kd
        
        if ftc == 'ke':
            from dbpedia_ent.dto.syn.n3.k import d_rev_ke
            return d_rev_ke
        
        if ftc == 'kf':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kf
            return d_rev_kf
        
        if ftc == 'kg':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kg
            return d_rev_kg
        
        if ftc == 'kh':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kh
            return d_rev_kh
        
        if ftc == 'ki':
            from dbpedia_ent.dto.syn.n3.k import d_rev_ki
            return d_rev_ki
        
        if ftc == 'kj':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kj
            return d_rev_kj
        
        if ftc == 'kk':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kk
            return d_rev_kk
        
        if ftc == 'kl':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kl
            return d_rev_kl
        
        if ftc == 'km':
            from dbpedia_ent.dto.syn.n3.k import d_rev_km
            return d_rev_km
        
        if ftc == 'kn':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kn
            return d_rev_kn
        
        if ftc == 'ko':
            from dbpedia_ent.dto.syn.n3.k import d_rev_ko
            return d_rev_ko
        
        if ftc == 'kp':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kp
            return d_rev_kp
        
        if ftc == 'kq':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kq
            return d_rev_kq
        
        if ftc == 'kr':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kr
            return d_rev_kr
        
        if ftc == 'ks':
            from dbpedia_ent.dto.syn.n3.k import d_rev_ks
            return d_rev_ks
        
        if ftc == 'kt':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kt
            return d_rev_kt
        
        if ftc == 'ku':
            from dbpedia_ent.dto.syn.n3.k import d_rev_ku
            return d_rev_ku
        
        if ftc == 'kv':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kv
            return d_rev_kv
        
        if ftc == 'kw':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kw
            return d_rev_kw
        
        if ftc == 'kx':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kx
            return d_rev_kx
        
        if ftc == 'ky':
            from dbpedia_ent.dto.syn.n3.k import d_rev_ky
            return d_rev_ky
        
        if ftc == 'kz':
            from dbpedia_ent.dto.syn.n3.k import d_rev_kz
            return d_rev_kz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        