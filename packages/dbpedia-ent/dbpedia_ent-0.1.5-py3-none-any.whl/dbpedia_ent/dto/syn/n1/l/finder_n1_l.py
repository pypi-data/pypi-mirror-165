
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1l(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'la':
            from dbpedia_ent.dto.syn.n1.l import d_rev_la
            return d_rev_la
        
        if ftc == 'lb':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lb
            return d_rev_lb
        
        if ftc == 'lc':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lc
            return d_rev_lc
        
        if ftc == 'ld':
            from dbpedia_ent.dto.syn.n1.l import d_rev_ld
            return d_rev_ld
        
        if ftc == 'le':
            from dbpedia_ent.dto.syn.n1.l import d_rev_le
            return d_rev_le
        
        if ftc == 'lf':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lf
            return d_rev_lf
        
        if ftc == 'lg':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lg
            return d_rev_lg
        
        if ftc == 'lh':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lh
            return d_rev_lh
        
        if ftc == 'li':
            from dbpedia_ent.dto.syn.n1.l import d_rev_li
            return d_rev_li
        
        if ftc == 'lj':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lj
            return d_rev_lj
        
        if ftc == 'lk':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lk
            return d_rev_lk
        
        if ftc == 'll':
            from dbpedia_ent.dto.syn.n1.l import d_rev_ll
            return d_rev_ll
        
        if ftc == 'lm':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lm
            return d_rev_lm
        
        if ftc == 'ln':
            from dbpedia_ent.dto.syn.n1.l import d_rev_ln
            return d_rev_ln
        
        if ftc == 'lo':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lo
            return d_rev_lo
        
        if ftc == 'lp':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lp
            return d_rev_lp
        
        if ftc == 'lq':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lq
            return d_rev_lq
        
        if ftc == 'lr':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lr
            return d_rev_lr
        
        if ftc == 'ls':
            from dbpedia_ent.dto.syn.n1.l import d_rev_ls
            return d_rev_ls
        
        if ftc == 'lt':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lt
            return d_rev_lt
        
        if ftc == 'lu':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lu
            return d_rev_lu
        
        if ftc == 'lv':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lv
            return d_rev_lv
        
        if ftc == 'lw':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lw
            return d_rev_lw
        
        if ftc == 'lx':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lx
            return d_rev_lx
        
        if ftc == 'ly':
            from dbpedia_ent.dto.syn.n1.l import d_rev_ly
            return d_rev_ly
        
        if ftc == 'lz':
            from dbpedia_ent.dto.syn.n1.l import d_rev_lz
            return d_rev_lz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        