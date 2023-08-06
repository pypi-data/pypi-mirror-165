
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN3q(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'q_':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_q_
                    return d_trie_q_
        
                if ftc == 'qa':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qa
                    return d_trie_qa
        
                if ftc == 'qb':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qb
                    return d_trie_qb
        
                if ftc == 'qc':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qc
                    return d_trie_qc
        
                if ftc == 'qd':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qd
                    return d_trie_qd
        
                if ftc == 'qe':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qe
                    return d_trie_qe
        
                if ftc == 'qf':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qf
                    return d_trie_qf
        
                # if ftc == 'qg':
                #     from dbpedia_ent.dto.ent.n3.q import d_trie_qg
                #     return d_trie_qg
        
                if ftc == 'qh':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qh
                    return d_trie_qh
        
                if ftc == 'qi':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qi
                    return d_trie_qi
        
                # if ftc == 'qj':
                #     from dbpedia_ent.dto.ent.n3.q import d_trie_qj
                #     return d_trie_qj
        
                # if ftc == 'qk':
                #     from dbpedia_ent.dto.ent.n3.q import d_trie_qk
                #     return d_trie_qk
        
                if ftc == 'ql':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_ql
                    return d_trie_ql
        
                if ftc == 'qm':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qm
                    return d_trie_qm
        
                if ftc == 'qn':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qn
                    return d_trie_qn
        
                if ftc == 'qo':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qo
                    return d_trie_qo
        
                if ftc == 'qp':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qp
                    return d_trie_qp
        
                if ftc == 'qq':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qq
                    return d_trie_qq
        
                if ftc == 'qr':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qr
                    return d_trie_qr
        
                if ftc == 'qs':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qs
                    return d_trie_qs
        
                if ftc == 'qt':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qt
                    return d_trie_qt
        
                if ftc == 'qu':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qu
                    return d_trie_qu
        
                if ftc == 'qv':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qv
                    return d_trie_qv
        
                if ftc == 'qw':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qw
                    return d_trie_qw
        
                # if ftc == 'qx':
                #     from dbpedia_ent.dto.ent.n3.q import d_trie_qx
                #     return d_trie_qx
        
                if ftc == 'qy':
                    from dbpedia_ent.dto.ent.n3.q import d_trie_qy
                    return d_trie_qy
        
                # if ftc == 'qz':
                #     from dbpedia_ent.dto.ent.n3.q import d_trie_qz
                #     return d_trie_qz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        