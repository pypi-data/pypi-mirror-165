
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN1o(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'oa':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oa
            return d_rev_oa
        
        if ftc == 'ob':
            from dbpedia_ent.dto.syn.n1.o import d_rev_ob
            return d_rev_ob
        
        if ftc == 'oc':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oc
            return d_rev_oc
        
        if ftc == 'od':
            from dbpedia_ent.dto.syn.n1.o import d_rev_od
            return d_rev_od
        
        if ftc == 'oe':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oe
            return d_rev_oe
        
        if ftc == 'of':
            from dbpedia_ent.dto.syn.n1.o import d_rev_of
            return d_rev_of
        
        if ftc == 'og':
            from dbpedia_ent.dto.syn.n1.o import d_rev_og
            return d_rev_og
        
        if ftc == 'oh':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oh
            return d_rev_oh
        
        if ftc == 'oi':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oi
            return d_rev_oi
        
        if ftc == 'oj':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oj
            return d_rev_oj
        
        if ftc == 'ok':
            from dbpedia_ent.dto.syn.n1.o import d_rev_ok
            return d_rev_ok
        
        if ftc == 'ol':
            from dbpedia_ent.dto.syn.n1.o import d_rev_ol
            return d_rev_ol
        
        if ftc == 'om':
            from dbpedia_ent.dto.syn.n1.o import d_rev_om
            return d_rev_om
        
        if ftc == 'on':
            from dbpedia_ent.dto.syn.n1.o import d_rev_on
            return d_rev_on
        
        if ftc == 'oo':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oo
            return d_rev_oo
        
        if ftc == 'op':
            from dbpedia_ent.dto.syn.n1.o import d_rev_op
            return d_rev_op
        
        if ftc == 'oq':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oq
            return d_rev_oq
        
        if ftc == 'or':
            from dbpedia_ent.dto.syn.n1.o import d_rev_or
            return d_rev_or
        
        if ftc == 'os':
            from dbpedia_ent.dto.syn.n1.o import d_rev_os
            return d_rev_os
        
        if ftc == 'ot':
            from dbpedia_ent.dto.syn.n1.o import d_rev_ot
            return d_rev_ot
        
        if ftc == 'ou':
            from dbpedia_ent.dto.syn.n1.o import d_rev_ou
            return d_rev_ou
        
        if ftc == 'ov':
            from dbpedia_ent.dto.syn.n1.o import d_rev_ov
            return d_rev_ov
        
        if ftc == 'ow':
            from dbpedia_ent.dto.syn.n1.o import d_rev_ow
            return d_rev_ow
        
        if ftc == 'ox':
            from dbpedia_ent.dto.syn.n1.o import d_rev_ox
            return d_rev_ox
        
        if ftc == 'oy':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oy
            return d_rev_oy
        
        if ftc == 'oz':
            from dbpedia_ent.dto.syn.n1.o import d_rev_oz
            return d_rev_oz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        