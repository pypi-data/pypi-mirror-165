
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN2e(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'e_':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_e_
                    return d_trie_e_
        
                if ftc == 'ea':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ea
                    return d_trie_ea
        
                if ftc == 'eb':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_eb
                    return d_trie_eb
        
                if ftc == 'ec':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ec
                    return d_trie_ec
        
                if ftc == 'ed':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ed
                    return d_trie_ed
        
                if ftc == 'ee':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ee
                    return d_trie_ee
        
                if ftc == 'ef':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ef
                    return d_trie_ef
        
                if ftc == 'eg':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_eg
                    return d_trie_eg
        
                if ftc == 'eh':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_eh
                    return d_trie_eh
        
                if ftc == 'ei':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ei
                    return d_trie_ei
        
                if ftc == 'ej':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ej
                    return d_trie_ej
        
                if ftc == 'ek':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ek
                    return d_trie_ek
        
                if ftc == 'el':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_el
                    return d_trie_el
        
                if ftc == 'em':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_em
                    return d_trie_em
        
                if ftc == 'en':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_en
                    return d_trie_en
        
                if ftc == 'eo':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_eo
                    return d_trie_eo
        
                if ftc == 'ep':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ep
                    return d_trie_ep
        
                if ftc == 'eq':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_eq
                    return d_trie_eq
        
                if ftc == 'er':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_er
                    return d_trie_er
        
                if ftc == 'es':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_es
                    return d_trie_es
        
                if ftc == 'et':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_et
                    return d_trie_et
        
                if ftc == 'eu':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_eu
                    return d_trie_eu
        
                if ftc == 'ev':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ev
                    return d_trie_ev
        
                if ftc == 'ew':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ew
                    return d_trie_ew
        
                if ftc == 'ex':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ex
                    return d_trie_ex
        
                if ftc == 'ey':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ey
                    return d_trie_ey
        
                if ftc == 'ez':
                    from dbpedia_ent.dto.ent.n2.e import d_trie_ez
                    return d_trie_ez
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        