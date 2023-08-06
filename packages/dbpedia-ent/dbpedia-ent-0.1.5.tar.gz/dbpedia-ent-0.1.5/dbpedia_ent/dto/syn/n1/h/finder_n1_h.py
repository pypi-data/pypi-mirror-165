
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1h(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ha':
            from dbpedia_ent.dto.syn.n1.h import d_rev_ha
            return d_rev_ha
        
        if ftc == 'hb':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hb
            return d_rev_hb
        
        if ftc == 'hc':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hc
            return d_rev_hc
        
        if ftc == 'hd':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hd
            return d_rev_hd
        
        if ftc == 'he':
            from dbpedia_ent.dto.syn.n1.h import d_rev_he
            return d_rev_he
        
        if ftc == 'hf':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hf
            return d_rev_hf
        
        if ftc == 'hg':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hg
            return d_rev_hg
        
        if ftc == 'hh':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hh
            return d_rev_hh
        
        if ftc == 'hi':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hi
            return d_rev_hi
        
        if ftc == 'hj':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hj
            return d_rev_hj
        
        if ftc == 'hk':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hk
            return d_rev_hk
        
        if ftc == 'hl':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hl
            return d_rev_hl
        
        if ftc == 'hm':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hm
            return d_rev_hm
        
        if ftc == 'hn':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hn
            return d_rev_hn
        
        if ftc == 'ho':
            from dbpedia_ent.dto.syn.n1.h import d_rev_ho
            return d_rev_ho
        
        if ftc == 'hp':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hp
            return d_rev_hp
        
        if ftc == 'hq':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hq
            return d_rev_hq
        
        if ftc == 'hr':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hr
            return d_rev_hr
        
        if ftc == 'hs':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hs
            return d_rev_hs
        
        if ftc == 'ht':
            from dbpedia_ent.dto.syn.n1.h import d_rev_ht
            return d_rev_ht
        
        if ftc == 'hu':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hu
            return d_rev_hu
        
        if ftc == 'hv':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hv
            return d_rev_hv
        
        if ftc == 'hw':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hw
            return d_rev_hw
        
        if ftc == 'hx':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hx
            return d_rev_hx
        
        if ftc == 'hy':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hy
            return d_rev_hy
        
        if ftc == 'hz':
            from dbpedia_ent.dto.syn.n1.h import d_rev_hz
            return d_rev_hz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        