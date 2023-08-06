
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN3s(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 's_':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_s_
                    return d_trie_s_
        
                if ftc == 'sa':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sa
                    return d_trie_sa
        
                if ftc == 'sb':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sb
                    return d_trie_sb
        
                if ftc == 'sc':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sc
                    return d_trie_sc
        
                if ftc == 'sd':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sd
                    return d_trie_sd
        
                if ftc == 'se':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_se
                    return d_trie_se
        
                if ftc == 'sf':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sf
                    return d_trie_sf
        
                if ftc == 'sg':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sg
                    return d_trie_sg
        
                if ftc == 'sh':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sh
                    return d_trie_sh
        
                if ftc == 'si':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_si
                    return d_trie_si
        
                if ftc == 'sj':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sj
                    return d_trie_sj
        
                if ftc == 'sk':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sk
                    return d_trie_sk
        
                if ftc == 'sl':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sl
                    return d_trie_sl
        
                if ftc == 'sm':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sm
                    return d_trie_sm
        
                if ftc == 'sn':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sn
                    return d_trie_sn
        
                if ftc == 'so':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_so
                    return d_trie_so
        
                if ftc == 'sp':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sp
                    return d_trie_sp
        
                if ftc == 'sq':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sq
                    return d_trie_sq
        
                if ftc == 'sr':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sr
                    return d_trie_sr
        
                if ftc == 'ss':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_ss
                    return d_trie_ss
        
                if ftc == 'st':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_st
                    return d_trie_st
        
                if ftc == 'su':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_su
                    return d_trie_su
        
                if ftc == 'sv':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sv
                    return d_trie_sv
        
                if ftc == 'sw':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sw
                    return d_trie_sw
        
                if ftc == 'sx':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sx
                    return d_trie_sx
        
                if ftc == 'sy':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sy
                    return d_trie_sy
        
                if ftc == 'sz':
                    from dbpedia_ent.dto.ent.n3.s import d_trie_sz
                    return d_trie_sz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        