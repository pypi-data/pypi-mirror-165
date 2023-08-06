
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import Callable


class SynFinderN2(object):

    __cache_finder = {}

    def _find_canon(self,
                    first_char: str) -> Callable:

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

        if first_char == 'a':
            from dbpedia_ent.dto.syn.n2.a import FinderN2a
            self.__cache_finder[first_char] = FinderN2a().find_canon

        if first_char == 'b':
            from dbpedia_ent.dto.syn.n2.b import FinderN2b
            self.__cache_finder[first_char] = FinderN2b().find_canon

        if first_char == 'c':
            from dbpedia_ent.dto.syn.n2.c import FinderN2c
            self.__cache_finder[first_char] = FinderN2c().find_canon

        if first_char == 'd':
            from dbpedia_ent.dto.syn.n2.d import FinderN2d
            self.__cache_finder[first_char] = FinderN2d().find_canon

        if first_char == 'e':
            from dbpedia_ent.dto.syn.n2.e import FinderN2e
            self.__cache_finder[first_char] = FinderN2e().find_canon

        if first_char == 'f':
            from dbpedia_ent.dto.syn.n2.f import FinderN2f
            self.__cache_finder[first_char] = FinderN2f().find_canon

        if first_char == 'g':
            from dbpedia_ent.dto.syn.n2.g import FinderN2g
            self.__cache_finder[first_char] = FinderN2g().find_canon

        if first_char == 'h':
            from dbpedia_ent.dto.syn.n2.h import FinderN2h
            self.__cache_finder[first_char] = FinderN2h().find_canon

        if first_char == 'i':
            from dbpedia_ent.dto.syn.n2.i import FinderN2i
            self.__cache_finder[first_char] = FinderN2i().find_canon

        if first_char == 'j':
            from dbpedia_ent.dto.syn.n2.j import FinderN2j
            self.__cache_finder[first_char] = FinderN2j().find_canon

        if first_char == 'k':
            from dbpedia_ent.dto.syn.n2.k import FinderN2k
            self.__cache_finder[first_char] = FinderN2k().find_canon

        if first_char == 'l':
            from dbpedia_ent.dto.syn.n2.l import FinderN2l
            self.__cache_finder[first_char] = FinderN2l().find_canon

        if first_char == 'm':
            from dbpedia_ent.dto.syn.n2.m import FinderN2m
            self.__cache_finder[first_char] = FinderN2m().find_canon

        if first_char == 'n':
            from dbpedia_ent.dto.syn.n2.n import FinderN2n
            self.__cache_finder[first_char] = FinderN2n().find_canon

        if first_char == 'o':
            from dbpedia_ent.dto.syn.n2.o import FinderN2o
            self.__cache_finder[first_char] = FinderN2o().find_canon

        if first_char == 'p':
            from dbpedia_ent.dto.syn.n2.p import FinderN2p
            self.__cache_finder[first_char] = FinderN2p().find_canon

        if first_char == 'q':
            from dbpedia_ent.dto.syn.n2.q import FinderN2q
            self.__cache_finder[first_char] = FinderN2q().find_canon

        if first_char == 'r':
            from dbpedia_ent.dto.syn.n2.r import FinderN2r
            self.__cache_finder[first_char] = FinderN2r().find_canon

        if first_char == 's':
            from dbpedia_ent.dto.syn.n2.s import FinderN2s
            self.__cache_finder[first_char] = FinderN2s().find_canon

        if first_char == 't':
            from dbpedia_ent.dto.syn.n2.t import FinderN2t
            self.__cache_finder[first_char] = FinderN2t().find_canon

        if first_char == 'u':
            from dbpedia_ent.dto.syn.n2.u import FinderN2u
            self.__cache_finder[first_char] = FinderN2u().find_canon

        if first_char == 'v':
            from dbpedia_ent.dto.syn.n2.v import FinderN2v
            self.__cache_finder[first_char] = FinderN2v().find_canon

        if first_char == 'w':
            from dbpedia_ent.dto.syn.n2.w import FinderN2w
            self.__cache_finder[first_char] = FinderN2w().find_canon

        if first_char == 'x':
            from dbpedia_ent.dto.syn.n2.x import FinderN2x
            self.__cache_finder[first_char] = FinderN2x().find_canon

        if first_char == 'y':
            from dbpedia_ent.dto.syn.n2.y import FinderN2y
            self.__cache_finder[first_char] = FinderN2y().find_canon

        if first_char == 'z':
            from dbpedia_ent.dto.syn.n2.z import FinderN2z
            self.__cache_finder[first_char] = FinderN2z().find_canon

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

    def find_canon(self,
                   input_text: str) -> bool:

        input_text = input_text.lower()
        exists_cb = self._find_canon(input_text[0])
        if exists_cb:
            return exists_cb(input_text)
