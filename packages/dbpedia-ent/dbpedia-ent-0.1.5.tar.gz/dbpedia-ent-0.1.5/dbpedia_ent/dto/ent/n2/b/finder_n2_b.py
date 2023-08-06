
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN2b(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'b_':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_b_
                    return d_trie_b_
        
                if ftc == 'ba':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_ba
                    return d_trie_ba
        
                if ftc == 'bb':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bb
                    return d_trie_bb
        
                if ftc == 'bc':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bc
                    return d_trie_bc
        
                if ftc == 'bd':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bd
                    return d_trie_bd
        
                if ftc == 'be':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_be
                    return d_trie_be
        
                if ftc == 'bf':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bf
                    return d_trie_bf
        
                if ftc == 'bg':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bg
                    return d_trie_bg
        
                if ftc == 'bh':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bh
                    return d_trie_bh
        
                if ftc == 'bi':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bi
                    return d_trie_bi
        
                if ftc == 'bj':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bj
                    return d_trie_bj
        
                if ftc == 'bk':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bk
                    return d_trie_bk
        
                if ftc == 'bl':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bl
                    return d_trie_bl
        
                if ftc == 'bm':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bm
                    return d_trie_bm
        
                if ftc == 'bn':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bn
                    return d_trie_bn
        
                if ftc == 'bo':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bo
                    return d_trie_bo
        
                if ftc == 'bp':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bp
                    return d_trie_bp
        
                if ftc == 'bq':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bq
                    return d_trie_bq
        
                if ftc == 'br':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_br
                    return d_trie_br
        
                if ftc == 'bs':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bs
                    return d_trie_bs
        
                if ftc == 'bt':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bt
                    return d_trie_bt
        
                if ftc == 'bu':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bu
                    return d_trie_bu
        
                if ftc == 'bv':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bv
                    return d_trie_bv
        
                if ftc == 'bw':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bw
                    return d_trie_bw
        
                if ftc == 'bx':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bx
                    return d_trie_bx
        
                if ftc == 'by':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_by
                    return d_trie_by
        
                if ftc == 'bz':
                    from dbpedia_ent.dto.ent.n2.b import d_trie_bz
                    return d_trie_bz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        