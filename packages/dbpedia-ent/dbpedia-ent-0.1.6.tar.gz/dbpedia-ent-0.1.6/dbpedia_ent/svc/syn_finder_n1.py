
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import Callable


class SynFinderN1(object):

    __cache_finder = {}

    def _find_canon(self,
                    first_char: str) -> Callable:

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

        if first_char == 'a':
            from dbpedia_ent.dto.syn.n1.a import FinderN1a
            self.__cache_finder[first_char] = FinderN1a().find_canon

        if first_char == 'b':
            from dbpedia_ent.dto.syn.n1.b import FinderN1b
            self.__cache_finder[first_char] = FinderN1b().find_canon

        if first_char == 'c':
            from dbpedia_ent.dto.syn.n1.c import FinderN1c
            self.__cache_finder[first_char] = FinderN1c().find_canon

        if first_char == 'd':
            from dbpedia_ent.dto.syn.n1.d import FinderN1d
            self.__cache_finder[first_char] = FinderN1d().find_canon

        if first_char == 'e':
            from dbpedia_ent.dto.syn.n1.e import FinderN1e
            self.__cache_finder[first_char] = FinderN1e().find_canon

        if first_char == 'f':
            from dbpedia_ent.dto.syn.n1.f import FinderN1f
            self.__cache_finder[first_char] = FinderN1f().find_canon

        if first_char == 'g':
            from dbpedia_ent.dto.syn.n1.g import FinderN1g
            self.__cache_finder[first_char] = FinderN1g().find_canon

        if first_char == 'h':
            from dbpedia_ent.dto.syn.n1.h import FinderN1h
            self.__cache_finder[first_char] = FinderN1h().find_canon

        if first_char == 'i':
            from dbpedia_ent.dto.syn.n1.i import FinderN1i
            self.__cache_finder[first_char] = FinderN1i().find_canon

        if first_char == 'j':
            from dbpedia_ent.dto.syn.n1.j import FinderN1j
            self.__cache_finder[first_char] = FinderN1j().find_canon

        if first_char == 'k':
            from dbpedia_ent.dto.syn.n1.k import FinderN1k
            self.__cache_finder[first_char] = FinderN1k().find_canon

        if first_char == 'l':
            from dbpedia_ent.dto.syn.n1.l import FinderN1l
            self.__cache_finder[first_char] = FinderN1l().find_canon

        if first_char == 'm':
            from dbpedia_ent.dto.syn.n1.m import FinderN1m
            self.__cache_finder[first_char] = FinderN1m().find_canon

        if first_char == 'n':
            from dbpedia_ent.dto.syn.n1.n import FinderN1n
            self.__cache_finder[first_char] = FinderN1n().find_canon

        if first_char == 'o':
            from dbpedia_ent.dto.syn.n1.o import FinderN1o
            self.__cache_finder[first_char] = FinderN1o().find_canon

        if first_char == 'p':
            from dbpedia_ent.dto.syn.n1.p import FinderN1p
            self.__cache_finder[first_char] = FinderN1p().find_canon

        if first_char == 'q':
            from dbpedia_ent.dto.syn.n1.q import FinderN1q
            self.__cache_finder[first_char] = FinderN1q().find_canon

        if first_char == 'r':
            from dbpedia_ent.dto.syn.n1.r import FinderN1r
            self.__cache_finder[first_char] = FinderN1r().find_canon

        if first_char == 's':
            from dbpedia_ent.dto.syn.n1.s import FinderN1s
            self.__cache_finder[first_char] = FinderN1s().find_canon

        if first_char == 't':
            from dbpedia_ent.dto.syn.n1.t import FinderN1t
            self.__cache_finder[first_char] = FinderN1t().find_canon

        if first_char == 'u':
            from dbpedia_ent.dto.syn.n1.u import FinderN1u
            self.__cache_finder[first_char] = FinderN1u().find_canon

        if first_char == 'v':
            from dbpedia_ent.dto.syn.n1.v import FinderN1v
            self.__cache_finder[first_char] = FinderN1v().find_canon

        if first_char == 'w':
            from dbpedia_ent.dto.syn.n1.w import FinderN1w
            self.__cache_finder[first_char] = FinderN1w().find_canon

        if first_char == 'x':
            from dbpedia_ent.dto.syn.n1.x import FinderN1x
            self.__cache_finder[first_char] = FinderN1x().find_canon

        if first_char == 'y':
            from dbpedia_ent.dto.syn.n1.y import FinderN1y
            self.__cache_finder[first_char] = FinderN1y().find_canon

        if first_char == 'z':
            from dbpedia_ent.dto.syn.n1.z import FinderN1z
            self.__cache_finder[first_char] = FinderN1z().find_canon

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

    def find_canon(self,
                   input_text: str) -> bool:

        input_text = input_text.lower()
        exists_cb = self._find_canon(input_text[0])
        if exists_cb:
            return exists_cb(input_text)
