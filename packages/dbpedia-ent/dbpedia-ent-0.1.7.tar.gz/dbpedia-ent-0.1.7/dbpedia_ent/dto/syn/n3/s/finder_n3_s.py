
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN3s(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'sa':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sa
            return d_rev_sa
        
        if ftc == 'sb':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sb
            return d_rev_sb
        
        if ftc == 'sc':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sc
            return d_rev_sc
        
        if ftc == 'sd':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sd
            return d_rev_sd
        
        if ftc == 'se':
            from dbpedia_ent.dto.syn.n3.s import d_rev_se
            return d_rev_se
        
        if ftc == 'sf':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sf
            return d_rev_sf
        
        if ftc == 'sg':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sg
            return d_rev_sg
        
        if ftc == 'sh':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sh
            return d_rev_sh
        
        if ftc == 'si':
            from dbpedia_ent.dto.syn.n3.s import d_rev_si
            return d_rev_si
        
        if ftc == 'sj':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sj
            return d_rev_sj
        
        if ftc == 'sk':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sk
            return d_rev_sk
        
        if ftc == 'sl':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sl
            return d_rev_sl
        
        if ftc == 'sm':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sm
            return d_rev_sm
        
        if ftc == 'sn':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sn
            return d_rev_sn
        
        if ftc == 'so':
            from dbpedia_ent.dto.syn.n3.s import d_rev_so
            return d_rev_so
        
        if ftc == 'sp':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sp
            return d_rev_sp
        
        if ftc == 'sq':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sq
            return d_rev_sq
        
        if ftc == 'sr':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sr
            return d_rev_sr
        
        if ftc == 'ss':
            from dbpedia_ent.dto.syn.n3.s import d_rev_ss
            return d_rev_ss
        
        if ftc == 'st':
            from dbpedia_ent.dto.syn.n3.s import d_rev_st
            return d_rev_st
        
        if ftc == 'su':
            from dbpedia_ent.dto.syn.n3.s import d_rev_su
            return d_rev_su
        
        if ftc == 'sv':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sv
            return d_rev_sv
        
        if ftc == 'sw':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sw
            return d_rev_sw
        
        if ftc == 'sx':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sx
            return d_rev_sx
        
        if ftc == 'sy':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sy
            return d_rev_sy
        
        if ftc == 'sz':
            from dbpedia_ent.dto.syn.n3.s import d_rev_sz
            return d_rev_sz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        