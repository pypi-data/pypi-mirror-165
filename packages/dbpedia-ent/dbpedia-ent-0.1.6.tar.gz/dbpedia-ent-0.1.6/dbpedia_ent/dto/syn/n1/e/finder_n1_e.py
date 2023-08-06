
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1e(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ea':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ea
            return d_rev_ea
        
        if ftc == 'eb':
            from dbpedia_ent.dto.syn.n1.e import d_rev_eb
            return d_rev_eb
        
        if ftc == 'ec':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ec
            return d_rev_ec
        
        if ftc == 'ed':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ed
            return d_rev_ed
        
        if ftc == 'ee':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ee
            return d_rev_ee
        
        if ftc == 'ef':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ef
            return d_rev_ef
        
        if ftc == 'eg':
            from dbpedia_ent.dto.syn.n1.e import d_rev_eg
            return d_rev_eg
        
        if ftc == 'eh':
            from dbpedia_ent.dto.syn.n1.e import d_rev_eh
            return d_rev_eh
        
        if ftc == 'ei':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ei
            return d_rev_ei
        
        if ftc == 'ej':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ej
            return d_rev_ej
        
        if ftc == 'ek':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ek
            return d_rev_ek
        
        if ftc == 'el':
            from dbpedia_ent.dto.syn.n1.e import d_rev_el
            return d_rev_el
        
        if ftc == 'em':
            from dbpedia_ent.dto.syn.n1.e import d_rev_em
            return d_rev_em
        
        if ftc == 'en':
            from dbpedia_ent.dto.syn.n1.e import d_rev_en
            return d_rev_en
        
        if ftc == 'eo':
            from dbpedia_ent.dto.syn.n1.e import d_rev_eo
            return d_rev_eo
        
        if ftc == 'ep':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ep
            return d_rev_ep
        
        if ftc == 'eq':
            from dbpedia_ent.dto.syn.n1.e import d_rev_eq
            return d_rev_eq
        
        if ftc == 'er':
            from dbpedia_ent.dto.syn.n1.e import d_rev_er
            return d_rev_er
        
        if ftc == 'es':
            from dbpedia_ent.dto.syn.n1.e import d_rev_es
            return d_rev_es
        
        if ftc == 'et':
            from dbpedia_ent.dto.syn.n1.e import d_rev_et
            return d_rev_et
        
        if ftc == 'eu':
            from dbpedia_ent.dto.syn.n1.e import d_rev_eu
            return d_rev_eu
        
        if ftc == 'ev':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ev
            return d_rev_ev
        
        if ftc == 'ew':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ew
            return d_rev_ew
        
        if ftc == 'ex':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ex
            return d_rev_ex
        
        if ftc == 'ey':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ey
            return d_rev_ey
        
        if ftc == 'ez':
            from dbpedia_ent.dto.syn.n1.e import d_rev_ez
            return d_rev_ez
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        