
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN2o(object):

    def _get_trie(self,
                ftc: str) -> dict:
        
                if ftc == 'o_':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_o_
                    return d_trie_o_
        
                if ftc == 'oa':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oa
                    return d_trie_oa
        
                if ftc == 'ob':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_ob
                    return d_trie_ob
        
                if ftc == 'oc':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oc
                    return d_trie_oc
        
                if ftc == 'od':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_od
                    return d_trie_od
        
                if ftc == 'oe':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oe
                    return d_trie_oe
        
                if ftc == 'of':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_of
                    return d_trie_of
        
                if ftc == 'og':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_og
                    return d_trie_og
        
                if ftc == 'oh':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oh
                    return d_trie_oh
        
                if ftc == 'oi':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oi
                    return d_trie_oi
        
                if ftc == 'oj':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oj
                    return d_trie_oj
        
                if ftc == 'ok':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_ok
                    return d_trie_ok
        
                if ftc == 'ol':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_ol
                    return d_trie_ol
        
                if ftc == 'om':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_om
                    return d_trie_om
        
                if ftc == 'on':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_on
                    return d_trie_on
        
                if ftc == 'oo':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oo
                    return d_trie_oo
        
                if ftc == 'op':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_op
                    return d_trie_op
        
                if ftc == 'oq':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oq
                    return d_trie_oq
        
                if ftc == 'or':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_or
                    return d_trie_or
        
                if ftc == 'os':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_os
                    return d_trie_os
        
                if ftc == 'ot':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_ot
                    return d_trie_ot
        
                if ftc == 'ou':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_ou
                    return d_trie_ou
        
                if ftc == 'ov':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_ov
                    return d_trie_ov
        
                if ftc == 'ow':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_ow
                    return d_trie_ow
        
                if ftc == 'ox':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_ox
                    return d_trie_ox
        
                if ftc == 'oy':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oy
                    return d_trie_oy
        
                if ftc == 'oz':
                    from dbpedia_ent.dto.ent.n2.o import d_trie_oz
                    return d_trie_oz
        

    def exists(self,
            input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
            input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
        