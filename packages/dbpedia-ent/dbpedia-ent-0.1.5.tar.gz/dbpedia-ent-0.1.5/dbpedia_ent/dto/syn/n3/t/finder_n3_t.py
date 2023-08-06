
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import find_canon


# AUTO GENERATED FINDER
class FinderN3t(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 'ta':
            from dbpedia_ent.dto.syn.n3.t import d_rev_ta
            return d_rev_ta
        
        if ftc == 'tb':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tb
            return d_rev_tb
        
        if ftc == 'tc':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tc
            return d_rev_tc
        
        if ftc == 'td':
            from dbpedia_ent.dto.syn.n3.t import d_rev_td
            return d_rev_td
        
        if ftc == 'te':
            from dbpedia_ent.dto.syn.n3.t import d_rev_te
            return d_rev_te
        
        if ftc == 'tf':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tf
            return d_rev_tf
        
        if ftc == 'tg':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tg
            return d_rev_tg
        
        if ftc == 'th':
            from dbpedia_ent.dto.syn.n3.t import d_rev_th
            return d_rev_th
        
        if ftc == 'ti':
            from dbpedia_ent.dto.syn.n3.t import d_rev_ti
            return d_rev_ti
        
        if ftc == 'tj':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tj
            return d_rev_tj
        
        if ftc == 'tk':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tk
            return d_rev_tk
        
        if ftc == 'tl':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tl
            return d_rev_tl
        
        if ftc == 'tm':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tm
            return d_rev_tm
        
        if ftc == 'tn':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tn
            return d_rev_tn
        
        if ftc == 'to':
            from dbpedia_ent.dto.syn.n3.t import d_rev_to
            return d_rev_to
        
        if ftc == 'tp':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tp
            return d_rev_tp
        
        if ftc == 'tq':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tq
            return d_rev_tq
        
        if ftc == 'tr':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tr
            return d_rev_tr
        
        if ftc == 'ts':
            from dbpedia_ent.dto.syn.n3.t import d_rev_ts
            return d_rev_ts
        
        if ftc == 'tt':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tt
            return d_rev_tt
        
        if ftc == 'tu':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tu
            return d_rev_tu
        
        if ftc == 'tv':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tv
            return d_rev_tv
        
        if ftc == 'tw':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tw
            return d_rev_tw
        
        if ftc == 'tx':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tx
            return d_rev_tx
        
        if ftc == 'ty':
            from dbpedia_ent.dto.syn.n3.t import d_rev_ty
            return d_rev_ty
        
        if ftc == 'tz':
            from dbpedia_ent.dto.syn.n3.t import d_rev_tz
            return d_rev_tz
        

    def find_canon(self,
               input_text: str) -> bool:
        return find_canon(input_text, self._get_trie)
        