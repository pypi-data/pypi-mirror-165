
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1f(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'fa':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fa
            return d_rev_fa
        
        if ftc == 'fb':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fb
            return d_rev_fb
        
        if ftc == 'fc':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fc
            return d_rev_fc
        
        if ftc == 'fd':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fd
            return d_rev_fd
        
        if ftc == 'fe':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fe
            return d_rev_fe
        
        if ftc == 'ff':
            from dbpedia_ent.dto.syn.n1.f import d_rev_ff
            return d_rev_ff
        
        if ftc == 'fg':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fg
            return d_rev_fg
        
        if ftc == 'fh':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fh
            return d_rev_fh
        
        if ftc == 'fi':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fi
            return d_rev_fi
        
        if ftc == 'fj':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fj
            return d_rev_fj
        
        if ftc == 'fk':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fk
            return d_rev_fk
        
        if ftc == 'fl':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fl
            return d_rev_fl
        
        if ftc == 'fm':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fm
            return d_rev_fm
        
        if ftc == 'fn':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fn
            return d_rev_fn
        
        if ftc == 'fo':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fo
            return d_rev_fo
        
        if ftc == 'fp':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fp
            return d_rev_fp
        
        if ftc == 'fq':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fq
            return d_rev_fq
        
        if ftc == 'fr':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fr
            return d_rev_fr
        
        if ftc == 'fs':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fs
            return d_rev_fs
        
        if ftc == 'ft':
            from dbpedia_ent.dto.syn.n1.f import d_rev_ft
            return d_rev_ft
        
        if ftc == 'fu':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fu
            return d_rev_fu
        
        if ftc == 'fv':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fv
            return d_rev_fv
        
        if ftc == 'fw':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fw
            return d_rev_fw
        
        if ftc == 'fx':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fx
            return d_rev_fx
        
        if ftc == 'fy':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fy
            return d_rev_fy
        
        if ftc == 'fz':
            from dbpedia_ent.dto.syn.n1.f import d_rev_fz
            return d_rev_fz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        