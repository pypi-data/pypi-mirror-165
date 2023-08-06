
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN2i(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ia':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ia
            return d_rev_ia
        
        if ftc == 'ib':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ib
            return d_rev_ib
        
        if ftc == 'ic':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ic
            return d_rev_ic
        
        if ftc == 'id':
            from dbpedia_ent.dto.syn.n2.i import d_rev_id
            return d_rev_id
        
        if ftc == 'ie':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ie
            return d_rev_ie
        
        if ftc == 'if':
            from dbpedia_ent.dto.syn.n2.i import d_rev_if
            return d_rev_if
        
        if ftc == 'ig':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ig
            return d_rev_ig
        
        if ftc == 'ih':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ih
            return d_rev_ih
        
        if ftc == 'ii':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ii
            return d_rev_ii
        
        if ftc == 'ij':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ij
            return d_rev_ij
        
        if ftc == 'ik':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ik
            return d_rev_ik
        
        if ftc == 'il':
            from dbpedia_ent.dto.syn.n2.i import d_rev_il
            return d_rev_il
        
        if ftc == 'im':
            from dbpedia_ent.dto.syn.n2.i import d_rev_im
            return d_rev_im
        
        if ftc == 'in':
            from dbpedia_ent.dto.syn.n2.i import d_rev_in
            return d_rev_in
        
        if ftc == 'io':
            from dbpedia_ent.dto.syn.n2.i import d_rev_io
            return d_rev_io
        
        if ftc == 'ip':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ip
            return d_rev_ip
        
        if ftc == 'iq':
            from dbpedia_ent.dto.syn.n2.i import d_rev_iq
            return d_rev_iq
        
        if ftc == 'ir':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ir
            return d_rev_ir
        
        if ftc == 'is':
            from dbpedia_ent.dto.syn.n2.i import d_rev_is
            return d_rev_is
        
        if ftc == 'it':
            from dbpedia_ent.dto.syn.n2.i import d_rev_it
            return d_rev_it
        
        if ftc == 'iu':
            from dbpedia_ent.dto.syn.n2.i import d_rev_iu
            return d_rev_iu
        
        if ftc == 'iv':
            from dbpedia_ent.dto.syn.n2.i import d_rev_iv
            return d_rev_iv
        
        if ftc == 'iw':
            from dbpedia_ent.dto.syn.n2.i import d_rev_iw
            return d_rev_iw
        
        if ftc == 'ix':
            from dbpedia_ent.dto.syn.n2.i import d_rev_ix
            return d_rev_ix
        
        if ftc == 'iy':
            from dbpedia_ent.dto.syn.n2.i import d_rev_iy
            return d_rev_iy
        
        if ftc == 'iz':
            from dbpedia_ent.dto.syn.n2.i import d_rev_iz
            return d_rev_iz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        