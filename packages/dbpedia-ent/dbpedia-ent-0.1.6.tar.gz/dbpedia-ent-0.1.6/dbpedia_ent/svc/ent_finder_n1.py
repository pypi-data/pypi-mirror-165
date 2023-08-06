
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import Callable


class EntFinderN1(object):

    __cache_exists = {}
    __cache_finder = {}

    def _get_finder(self,
                    first_char: str) -> Callable:

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

        if first_char == 'a':
            from dbpedia_ent.dto.ent.n1.a import FinderN1a
            self.__cache_finder[first_char] = FinderN1a().find

        if first_char == 'b':
            from dbpedia_ent.dto.ent.n1.b import FinderN1b
            self.__cache_finder[first_char] = FinderN1b().find

        if first_char == 'c':
            from dbpedia_ent.dto.ent.n1.c import FinderN1c
            self.__cache_finder[first_char] = FinderN1c().find

        if first_char == 'd':
            from dbpedia_ent.dto.ent.n1.d import FinderN1d
            self.__cache_finder[first_char] = FinderN1d().find

        if first_char == 'e':
            from dbpedia_ent.dto.ent.n1.e import FinderN1e
            self.__cache_finder[first_char] = FinderN1e().find

        if first_char == 'f':
            from dbpedia_ent.dto.ent.n1.f import FinderN1f
            self.__cache_finder[first_char] = FinderN1f().find

        if first_char == 'g':
            from dbpedia_ent.dto.ent.n1.g import FinderN1g
            self.__cache_finder[first_char] = FinderN1g().find

        if first_char == 'h':
            from dbpedia_ent.dto.ent.n1.h import FinderN1h
            self.__cache_finder[first_char] = FinderN1h().find

        if first_char == 'i':
            from dbpedia_ent.dto.ent.n1.i import FinderN1i
            self.__cache_finder[first_char] = FinderN1i().find

        if first_char == 'j':
            from dbpedia_ent.dto.ent.n1.j import FinderN1j
            self.__cache_finder[first_char] = FinderN1j().find

        if first_char == 'k':
            from dbpedia_ent.dto.ent.n1.k import FinderN1k
            self.__cache_finder[first_char] = FinderN1k().find

        if first_char == 'l':
            from dbpedia_ent.dto.ent.n1.l import FinderN1l
            self.__cache_finder[first_char] = FinderN1l().find

        if first_char == 'm':
            from dbpedia_ent.dto.ent.n1.m import FinderN1m
            self.__cache_finder[first_char] = FinderN1m().find

        if first_char == 'n':
            from dbpedia_ent.dto.ent.n1.n import FinderN1n
            self.__cache_finder[first_char] = FinderN1n().find

        if first_char == 'o':
            from dbpedia_ent.dto.ent.n1.o import FinderN1o
            self.__cache_finder[first_char] = FinderN1o().find

        if first_char == 'p':
            from dbpedia_ent.dto.ent.n1.p import FinderN1p
            self.__cache_finder[first_char] = FinderN1p().find

        if first_char == 'q':
            from dbpedia_ent.dto.ent.n1.q import FinderN1q
            self.__cache_finder[first_char] = FinderN1q().find

        if first_char == 'r':
            from dbpedia_ent.dto.ent.n1.r import FinderN1r
            self.__cache_finder[first_char] = FinderN1r().find

        if first_char == 's':
            from dbpedia_ent.dto.ent.n1.s import FinderN1s
            self.__cache_finder[first_char] = FinderN1s().find

        if first_char == 't':
            from dbpedia_ent.dto.ent.n1.t import FinderN1t
            self.__cache_finder[first_char] = FinderN1t().find

        if first_char == 'u':
            from dbpedia_ent.dto.ent.n1.u import FinderN1u
            self.__cache_finder[first_char] = FinderN1u().find

        if first_char == 'v':
            from dbpedia_ent.dto.ent.n1.v import FinderN1v
            self.__cache_finder[first_char] = FinderN1v().find

        if first_char == 'w':
            from dbpedia_ent.dto.ent.n1.w import FinderN1w
            self.__cache_finder[first_char] = FinderN1w().find

        if first_char == 'x':
            from dbpedia_ent.dto.ent.n1.x import FinderN1x
            self.__cache_finder[first_char] = FinderN1x().find

        if first_char == 'y':
            from dbpedia_ent.dto.ent.n1.y import FinderN1y
            self.__cache_finder[first_char] = FinderN1y().find

        if first_char == 'z':
            from dbpedia_ent.dto.ent.n1.z import FinderN1z
            self.__cache_finder[first_char] = FinderN1z().find

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

    def _get_exists(self,
                    first_char: str) -> Callable:

        if first_char in self.__cache_exists:
            return self.__cache_exists[first_char]

        if first_char == 'a':
            from dbpedia_ent.dto.ent.n1.a import FinderN1a
            self.__cache_exists[first_char] = FinderN1a().exists

        if first_char == 'b':
            from dbpedia_ent.dto.ent.n1.b import FinderN1b
            self.__cache_exists[first_char] = FinderN1b().exists

        if first_char == 'c':
            from dbpedia_ent.dto.ent.n1.c import FinderN1c
            self.__cache_exists[first_char] = FinderN1c().exists

        if first_char == 'd':
            from dbpedia_ent.dto.ent.n1.d import FinderN1d
            self.__cache_exists[first_char] = FinderN1d().exists

        if first_char == 'e':
            from dbpedia_ent.dto.ent.n1.e import FinderN1e
            self.__cache_exists[first_char] = FinderN1e().exists

        if first_char == 'f':
            from dbpedia_ent.dto.ent.n1.f import FinderN1f
            self.__cache_exists[first_char] = FinderN1f().exists

        if first_char == 'g':
            from dbpedia_ent.dto.ent.n1.g import FinderN1g
            self.__cache_exists[first_char] = FinderN1g().exists

        if first_char == 'h':
            from dbpedia_ent.dto.ent.n1.h import FinderN1h
            self.__cache_exists[first_char] = FinderN1h().exists

        if first_char == 'i':
            from dbpedia_ent.dto.ent.n1.i import FinderN1i
            self.__cache_exists[first_char] = FinderN1i().exists

        if first_char == 'j':
            from dbpedia_ent.dto.ent.n1.j import FinderN1j
            self.__cache_exists[first_char] = FinderN1j().exists

        if first_char == 'k':
            from dbpedia_ent.dto.ent.n1.k import FinderN1k
            self.__cache_exists[first_char] = FinderN1k().exists

        if first_char == 'l':
            from dbpedia_ent.dto.ent.n1.l import FinderN1l
            self.__cache_exists[first_char] = FinderN1l().exists

        if first_char == 'm':
            from dbpedia_ent.dto.ent.n1.m import FinderN1m
            self.__cache_exists[first_char] = FinderN1m().exists

        if first_char == 'n':
            from dbpedia_ent.dto.ent.n1.n import FinderN1n
            self.__cache_exists[first_char] = FinderN1n().exists

        if first_char == 'o':
            from dbpedia_ent.dto.ent.n1.o import FinderN1o
            self.__cache_exists[first_char] = FinderN1o().exists

        if first_char == 'p':
            from dbpedia_ent.dto.ent.n1.p import FinderN1p
            self.__cache_exists[first_char] = FinderN1p().exists

        if first_char == 'q':
            from dbpedia_ent.dto.ent.n1.q import FinderN1q
            self.__cache_exists[first_char] = FinderN1q().exists

        if first_char == 'r':
            from dbpedia_ent.dto.ent.n1.r import FinderN1r
            self.__cache_exists[first_char] = FinderN1r().exists

        if first_char == 's':
            from dbpedia_ent.dto.ent.n1.s import FinderN1s
            self.__cache_exists[first_char] = FinderN1s().exists

        if first_char == 't':
            from dbpedia_ent.dto.ent.n1.t import FinderN1t
            self.__cache_exists[first_char] = FinderN1t().exists

        if first_char == 'u':
            from dbpedia_ent.dto.ent.n1.u import FinderN1u
            self.__cache_exists[first_char] = FinderN1u().exists

        if first_char == 'v':
            from dbpedia_ent.dto.ent.n1.v import FinderN1v
            self.__cache_exists[first_char] = FinderN1v().exists

        if first_char == 'w':
            from dbpedia_ent.dto.ent.n1.w import FinderN1w
            self.__cache_exists[first_char] = FinderN1w().exists

        if first_char == 'x':
            from dbpedia_ent.dto.ent.n1.x import FinderN1x
            self.__cache_exists[first_char] = FinderN1x().exists

        if first_char == 'y':
            from dbpedia_ent.dto.ent.n1.y import FinderN1y
            self.__cache_exists[first_char] = FinderN1y().exists

        if first_char == 'z':
            from dbpedia_ent.dto.ent.n1.z import FinderN1z
            self.__cache_exists[first_char] = FinderN1z().exists

        if first_char in self.__cache_exists:
            return self.__cache_exists[first_char]

    def exists(self,
               input_text: str) -> bool:

        input_text = input_text.lower()
        exists_cb = self._get_exists(input_text[0])
        if exists_cb:
            return exists_cb(input_text)

    def find(self,
             input_text: str) -> bool:

        input_text = input_text.lower()
        finde_cb = self._get_finder(input_text[0])
        if finde_cb:
            return finde_cb(input_text)
