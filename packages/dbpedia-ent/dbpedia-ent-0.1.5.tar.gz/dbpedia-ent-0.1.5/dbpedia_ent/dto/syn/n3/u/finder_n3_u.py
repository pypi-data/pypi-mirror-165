
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN3u(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ua':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ua
            return d_rev_ua
        
        if ftc == 'ub':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ub
            return d_rev_ub
        
        if ftc == 'uc':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uc
            return d_rev_uc
        
        if ftc == 'ud':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ud
            return d_rev_ud
        
        if ftc == 'ue':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ue
            return d_rev_ue
        
        if ftc == 'uf':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uf
            return d_rev_uf
        
        if ftc == 'ug':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ug
            return d_rev_ug
        
        if ftc == 'uh':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uh
            return d_rev_uh
        
        if ftc == 'ui':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ui
            return d_rev_ui
        
        if ftc == 'uj':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uj
            return d_rev_uj
        
        if ftc == 'uk':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uk
            return d_rev_uk
        
        if ftc == 'ul':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ul
            return d_rev_ul
        
        if ftc == 'um':
            from dbpedia_ent.dto.syn.n3.u import d_rev_um
            return d_rev_um
        
        if ftc == 'un':
            from dbpedia_ent.dto.syn.n3.u import d_rev_un
            return d_rev_un
        
        if ftc == 'uo':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uo
            return d_rev_uo
        
        if ftc == 'up':
            from dbpedia_ent.dto.syn.n3.u import d_rev_up
            return d_rev_up
        
        if ftc == 'uq':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uq
            return d_rev_uq
        
        if ftc == 'ur':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ur
            return d_rev_ur
        
        if ftc == 'us':
            from dbpedia_ent.dto.syn.n3.u import d_rev_us
            return d_rev_us
        
        if ftc == 'ut':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ut
            return d_rev_ut
        
        if ftc == 'uu':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uu
            return d_rev_uu
        
        if ftc == 'uv':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uv
            return d_rev_uv
        
        if ftc == 'uw':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uw
            return d_rev_uw
        
        if ftc == 'ux':
            from dbpedia_ent.dto.syn.n3.u import d_rev_ux
            return d_rev_ux
        
        if ftc == 'uy':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uy
            return d_rev_uy
        
        if ftc == 'uz':
            from dbpedia_ent.dto.syn.n3.u import d_rev_uz
            return d_rev_uz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        