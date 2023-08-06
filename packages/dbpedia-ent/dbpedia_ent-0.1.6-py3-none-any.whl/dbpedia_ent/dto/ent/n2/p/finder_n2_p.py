
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN2p(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'p_':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_p_
                    return d_trie_p_
        
                if ftc == 'pa':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pa
                    return d_trie_pa
        
                if ftc == 'pb':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pb
                    return d_trie_pb
        
                if ftc == 'pc':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pc
                    return d_trie_pc
        
                if ftc == 'pd':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pd
                    return d_trie_pd
        
                if ftc == 'pe':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pe
                    return d_trie_pe
        
                if ftc == 'pf':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pf
                    return d_trie_pf
        
                if ftc == 'pg':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pg
                    return d_trie_pg
        
                if ftc == 'ph':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_ph
                    return d_trie_ph
        
                if ftc == 'pi':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pi
                    return d_trie_pi
        
                if ftc == 'pj':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pj
                    return d_trie_pj
        
                if ftc == 'pk':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pk
                    return d_trie_pk
        
                if ftc == 'pl':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pl
                    return d_trie_pl
        
                if ftc == 'pm':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pm
                    return d_trie_pm
        
                if ftc == 'pn':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pn
                    return d_trie_pn
        
                if ftc == 'po':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_po
                    return d_trie_po
        
                if ftc == 'pp':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pp
                    return d_trie_pp
        
                if ftc == 'pq':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pq
                    return d_trie_pq
        
                if ftc == 'pr':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pr
                    return d_trie_pr
        
                if ftc == 'ps':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_ps
                    return d_trie_ps
        
                if ftc == 'pt':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pt
                    return d_trie_pt
        
                if ftc == 'pu':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pu
                    return d_trie_pu
        
                if ftc == 'pv':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pv
                    return d_trie_pv
        
                if ftc == 'pw':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pw
                    return d_trie_pw
        
                if ftc == 'px':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_px
                    return d_trie_px
        
                if ftc == 'py':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_py
                    return d_trie_py
        
                if ftc == 'pz':
                    from dbpedia_ent.dto.ent.n2.p import d_trie_pz
                    return d_trie_pz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        