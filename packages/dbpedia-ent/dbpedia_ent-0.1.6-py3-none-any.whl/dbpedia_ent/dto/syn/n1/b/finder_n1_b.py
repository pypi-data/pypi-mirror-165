
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1b(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ba':
            from dbpedia_ent.dto.syn.n1.b import d_rev_ba
            return d_rev_ba
        
        if ftc == 'bb':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bb
            return d_rev_bb
        
        if ftc == 'bc':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bc
            return d_rev_bc
        
        if ftc == 'bd':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bd
            return d_rev_bd
        
        if ftc == 'be':
            from dbpedia_ent.dto.syn.n1.b import d_rev_be
            return d_rev_be
        
        if ftc == 'bf':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bf
            return d_rev_bf
        
        if ftc == 'bg':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bg
            return d_rev_bg
        
        if ftc == 'bh':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bh
            return d_rev_bh
        
        if ftc == 'bi':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bi
            return d_rev_bi
        
        if ftc == 'bj':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bj
            return d_rev_bj
        
        if ftc == 'bk':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bk
            return d_rev_bk
        
        if ftc == 'bl':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bl
            return d_rev_bl
        
        if ftc == 'bm':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bm
            return d_rev_bm
        
        if ftc == 'bn':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bn
            return d_rev_bn
        
        if ftc == 'bo':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bo
            return d_rev_bo
        
        if ftc == 'bp':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bp
            return d_rev_bp
        
        if ftc == 'bq':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bq
            return d_rev_bq
        
        if ftc == 'br':
            from dbpedia_ent.dto.syn.n1.b import d_rev_br
            return d_rev_br
        
        if ftc == 'bs':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bs
            return d_rev_bs
        
        if ftc == 'bt':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bt
            return d_rev_bt
        
        if ftc == 'bu':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bu
            return d_rev_bu
        
        if ftc == 'bv':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bv
            return d_rev_bv
        
        if ftc == 'bw':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bw
            return d_rev_bw
        
        if ftc == 'bx':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bx
            return d_rev_bx
        
        if ftc == 'by':
            from dbpedia_ent.dto.syn.n1.b import d_rev_by
            return d_rev_by
        
        if ftc == 'bz':
            from dbpedia_ent.dto.syn.n1.b import d_rev_bz
            return d_rev_bz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        