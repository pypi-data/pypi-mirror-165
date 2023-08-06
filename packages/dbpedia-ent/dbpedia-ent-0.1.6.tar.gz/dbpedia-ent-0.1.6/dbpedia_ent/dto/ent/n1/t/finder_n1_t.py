
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_ent.dmo import ngram_exists
from dbpedia_ent.dmo import ngram_finder


# AUTO GENERATED FINDER
class FinderN1t(object):

    def _get_trie(self,
                  ftc: str) -> dict:
        
        if ftc == 't_':
            from dbpedia_ent.dto.ent.n1.t import d_trie_t_
            return d_trie_t_

        if ftc == 'ta':
            from dbpedia_ent.dto.ent.n1.t import d_trie_ta
            return d_trie_ta

        if ftc == 'tb':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tb
            return d_trie_tb

        if ftc == 'tc':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tc
            return d_trie_tc

        if ftc == 'td':
            from dbpedia_ent.dto.ent.n1.t import d_trie_td
            return d_trie_td

        if ftc == 'te':
            from dbpedia_ent.dto.ent.n1.t import d_trie_te
            return d_trie_te

        if ftc == 'tf':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tf
            return d_trie_tf

        if ftc == 'tg':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tg
            return d_trie_tg

        if ftc == 'th':
            from dbpedia_ent.dto.ent.n1.t import d_trie_th
            return d_trie_th

        if ftc == 'ti':
            from dbpedia_ent.dto.ent.n1.t import d_trie_ti
            return d_trie_ti

        if ftc == 'tj':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tj
            return d_trie_tj

        if ftc == 'tk':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tk
            return d_trie_tk

        if ftc == 'tl':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tl
            return d_trie_tl

        if ftc == 'tm':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tm
            return d_trie_tm

        if ftc == 'tn':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tn
            return d_trie_tn

        if ftc == 'to':
            from dbpedia_ent.dto.ent.n1.t import d_trie_to
            return d_trie_to

        if ftc == 'tp':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tp
            return d_trie_tp

        if ftc == 'tq':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tq
            return d_trie_tq

        if ftc == 'tr':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tr
            return d_trie_tr

        if ftc == 'ts':
            from dbpedia_ent.dto.ent.n1.t import d_trie_ts
            return d_trie_ts

        if ftc == 'tt':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tt
            return d_trie_tt

        if ftc == 'tu':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tu
            return d_trie_tu

        if ftc == 'tv':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tv
            return d_trie_tv

        if ftc == 'tw':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tw
            return d_trie_tw

        if ftc == 'tx':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tx
            return d_trie_tx

        if ftc == 'ty':
            from dbpedia_ent.dto.ent.n1.t import d_trie_ty
            return d_trie_ty

        if ftc == 'tz':
            from dbpedia_ent.dto.ent.n1.t import d_trie_tz
            return d_trie_tz


    def exists(self,
               input_text: str) -> bool:
        return ngram_exists(input_text=input_text,
                            d_trie_finder=self._get_trie)

    def find(self,
             input_text: str) -> bool:
        return ngram_finder(input_text=input_text,
                            d_trie_finder=self._get_trie)
