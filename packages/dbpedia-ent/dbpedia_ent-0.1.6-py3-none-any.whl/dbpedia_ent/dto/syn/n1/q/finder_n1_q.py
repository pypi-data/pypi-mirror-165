
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1q(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'qa':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qa
            return d_rev_qa
        
        if ftc == 'qb':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qb
            return d_rev_qb
        
        if ftc == 'qc':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qc
            return d_rev_qc
        
        if ftc == 'qd':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qd
            return d_rev_qd
        
        if ftc == 'qe':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qe
            return d_rev_qe
        
        if ftc == 'qf':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qf
            return d_rev_qf
        
        if ftc == 'qg':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qg
            return d_rev_qg
        
        if ftc == 'qh':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qh
            return d_rev_qh
        
        if ftc == 'qi':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qi
            return d_rev_qi
        
        if ftc == 'qj':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qj
            return d_rev_qj
        
        if ftc == 'qk':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qk
            return d_rev_qk
        
        if ftc == 'ql':
            from dbpedia_ent.dto.syn.n1.q import d_rev_ql
            return d_rev_ql
        
        if ftc == 'qm':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qm
            return d_rev_qm
        
        if ftc == 'qn':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qn
            return d_rev_qn
        
        if ftc == 'qo':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qo
            return d_rev_qo
        
        if ftc == 'qp':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qp
            return d_rev_qp
        
        if ftc == 'qq':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qq
            return d_rev_qq
        
        if ftc == 'qr':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qr
            return d_rev_qr
        
        if ftc == 'qs':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qs
            return d_rev_qs
        
        if ftc == 'qt':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qt
            return d_rev_qt
        
        if ftc == 'qu':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qu
            return d_rev_qu
        
        if ftc == 'qv':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qv
            return d_rev_qv
        
        if ftc == 'qw':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qw
            return d_rev_qw
        
        if ftc == 'qx':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qx
            return d_rev_qx
        
        if ftc == 'qy':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qy
            return d_rev_qy
        
        if ftc == 'qz':
            from dbpedia_ent.dto.syn.n1.q import d_rev_qz
            return d_rev_qz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        