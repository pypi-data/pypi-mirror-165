
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN2i(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'i_':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_i_
                    return d_trie_i_
        
                if ftc == 'ia':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ia
                    return d_trie_ia
        
                if ftc == 'ib':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ib
                    return d_trie_ib
        
                if ftc == 'ic':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ic
                    return d_trie_ic
        
                if ftc == 'id':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_id
                    return d_trie_id
        
                if ftc == 'ie':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ie
                    return d_trie_ie
        
                if ftc == 'if':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_if
                    return d_trie_if
        
                if ftc == 'ig':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ig
                    return d_trie_ig
        
                if ftc == 'ih':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ih
                    return d_trie_ih
        
                if ftc == 'ii':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ii
                    return d_trie_ii
        
                if ftc == 'ij':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ij
                    return d_trie_ij
        
                if ftc == 'ik':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ik
                    return d_trie_ik
        
                if ftc == 'il':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_il
                    return d_trie_il
        
                if ftc == 'im':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_im
                    return d_trie_im
        
                if ftc == 'in':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_in
                    return d_trie_in
        
                if ftc == 'io':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_io
                    return d_trie_io
        
                if ftc == 'ip':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ip
                    return d_trie_ip
        
                if ftc == 'iq':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_iq
                    return d_trie_iq
        
                if ftc == 'ir':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ir
                    return d_trie_ir
        
                if ftc == 'is':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_is
                    return d_trie_is
        
                if ftc == 'it':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_it
                    return d_trie_it
        
                if ftc == 'iu':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_iu
                    return d_trie_iu
        
                if ftc == 'iv':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_iv
                    return d_trie_iv
        
                if ftc == 'iw':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_iw
                    return d_trie_iw
        
                if ftc == 'ix':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_ix
                    return d_trie_ix
        
                if ftc == 'iy':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_iy
                    return d_trie_iy
        
                if ftc == 'iz':
                    from dbpedia_ent.dto.ent.n2.i import d_trie_iz
                    return d_trie_iz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        