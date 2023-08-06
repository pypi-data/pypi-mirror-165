
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import Callable


class EntFinderN2(object):

    __cache_exists = {}
    __cache_finder = {}

    def _get_finder(self,
                    first_char: str) -> Callable:

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

        if first_char == 'a':
            from dbpedia_ent.dto.ent.n2.a import FinderN2a
            self.__cache_finder[first_char] = FinderN2a().find

        if first_char == 'b':
            from dbpedia_ent.dto.ent.n2.b import FinderN2b
            self.__cache_finder[first_char] = FinderN2b().find

        if first_char == 'c':
            from dbpedia_ent.dto.ent.n2.c import FinderN2c
            self.__cache_finder[first_char] = FinderN2c().find

        if first_char == 'd':
            from dbpedia_ent.dto.ent.n2.d import FinderN2d
            self.__cache_finder[first_char] = FinderN2d().find

        if first_char == 'e':
            from dbpedia_ent.dto.ent.n2.e import FinderN2e
            self.__cache_finder[first_char] = FinderN2e().find

        if first_char == 'f':
            from dbpedia_ent.dto.ent.n2.f import FinderN2f
            self.__cache_finder[first_char] = FinderN2f().find

        if first_char == 'g':
            from dbpedia_ent.dto.ent.n2.g import FinderN2g
            self.__cache_finder[first_char] = FinderN2g().find

        if first_char == 'h':
            from dbpedia_ent.dto.ent.n2.h import FinderN2h
            self.__cache_finder[first_char] = FinderN2h().find

        if first_char == 'i':
            from dbpedia_ent.dto.ent.n2.i import FinderN2i
            self.__cache_finder[first_char] = FinderN2i().find

        if first_char == 'j':
            from dbpedia_ent.dto.ent.n2.j import FinderN2j
            self.__cache_finder[first_char] = FinderN2j().find

        if first_char == 'k':
            from dbpedia_ent.dto.ent.n2.k import FinderN2k
            self.__cache_finder[first_char] = FinderN2k().find

        if first_char == 'l':
            from dbpedia_ent.dto.ent.n2.l import FinderN2l
            self.__cache_finder[first_char] = FinderN2l().find

        if first_char == 'm':
            from dbpedia_ent.dto.ent.n2.m import FinderN2m
            self.__cache_finder[first_char] = FinderN2m().find

        if first_char == 'n':
            from dbpedia_ent.dto.ent.n2.n import FinderN2n
            self.__cache_finder[first_char] = FinderN2n().find

        if first_char == 'o':
            from dbpedia_ent.dto.ent.n2.o import FinderN2o
            self.__cache_finder[first_char] = FinderN2o().find

        if first_char == 'p':
            from dbpedia_ent.dto.ent.n2.p import FinderN2p
            self.__cache_finder[first_char] = FinderN2p().find

        if first_char == 'q':
            from dbpedia_ent.dto.ent.n2.q import FinderN2q
            self.__cache_finder[first_char] = FinderN2q().find

        if first_char == 'r':
            from dbpedia_ent.dto.ent.n2.r import FinderN2r
            self.__cache_finder[first_char] = FinderN2r().find

        if first_char == 's':
            from dbpedia_ent.dto.ent.n2.s import FinderN2s
            self.__cache_finder[first_char] = FinderN2s().find

        if first_char == 't':
            from dbpedia_ent.dto.ent.n2.t import FinderN2t
            self.__cache_finder[first_char] = FinderN2t().find

        if first_char == 'u':
            from dbpedia_ent.dto.ent.n2.u import FinderN2u
            self.__cache_finder[first_char] = FinderN2u().find

        if first_char == 'v':
            from dbpedia_ent.dto.ent.n2.v import FinderN2v
            self.__cache_finder[first_char] = FinderN2v().find

        if first_char == 'w':
            from dbpedia_ent.dto.ent.n2.w import FinderN2w
            self.__cache_finder[first_char] = FinderN2w().find

        if first_char == 'x':
            from dbpedia_ent.dto.ent.n2.x import FinderN2x
            self.__cache_finder[first_char] = FinderN2x().find

        if first_char == 'y':
            from dbpedia_ent.dto.ent.n2.y import FinderN2y
            self.__cache_finder[first_char] = FinderN2y().find

        if first_char == 'z':
            from dbpedia_ent.dto.ent.n2.z import FinderN2z
            self.__cache_finder[first_char] = FinderN2z().find

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

    def _get_exists(self,
                    first_char: str) -> Callable:

        if first_char in self.__cache_exists:
            return self.__cache_exists[first_char]

        if first_char == 'a':
            from dbpedia_ent.dto.ent.n2.a import FinderN2a
            self.__cache_exists[first_char] = FinderN2a().exists

        if first_char == 'b':
            from dbpedia_ent.dto.ent.n2.b import FinderN2b
            self.__cache_exists[first_char] = FinderN2b().exists

        if first_char == 'c':
            from dbpedia_ent.dto.ent.n2.c import FinderN2c
            self.__cache_exists[first_char] = FinderN2c().exists

        if first_char == 'd':
            from dbpedia_ent.dto.ent.n2.d import FinderN2d
            self.__cache_exists[first_char] = FinderN2d().exists

        if first_char == 'e':
            from dbpedia_ent.dto.ent.n2.e import FinderN2e
            self.__cache_exists[first_char] = FinderN2e().exists

        if first_char == 'f':
            from dbpedia_ent.dto.ent.n2.f import FinderN2f
            self.__cache_exists[first_char] = FinderN2f().exists

        if first_char == 'g':
            from dbpedia_ent.dto.ent.n2.g import FinderN2g
            self.__cache_exists[first_char] = FinderN2g().exists

        if first_char == 'h':
            from dbpedia_ent.dto.ent.n2.h import FinderN2h
            self.__cache_exists[first_char] = FinderN2h().exists

        if first_char == 'i':
            from dbpedia_ent.dto.ent.n2.i import FinderN2i
            self.__cache_exists[first_char] = FinderN2i().exists

        if first_char == 'j':
            from dbpedia_ent.dto.ent.n2.j import FinderN2j
            self.__cache_exists[first_char] = FinderN2j().exists

        if first_char == 'k':
            from dbpedia_ent.dto.ent.n2.k import FinderN2k
            self.__cache_exists[first_char] = FinderN2k().exists

        if first_char == 'l':
            from dbpedia_ent.dto.ent.n2.l import FinderN2l
            self.__cache_exists[first_char] = FinderN2l().exists

        if first_char == 'm':
            from dbpedia_ent.dto.ent.n2.m import FinderN2m
            self.__cache_exists[first_char] = FinderN2m().exists

        if first_char == 'n':
            from dbpedia_ent.dto.ent.n2.n import FinderN2n
            self.__cache_exists[first_char] = FinderN2n().exists

        if first_char == 'o':
            from dbpedia_ent.dto.ent.n2.o import FinderN2o
            self.__cache_exists[first_char] = FinderN2o().exists

        if first_char == 'p':
            from dbpedia_ent.dto.ent.n2.p import FinderN2p
            self.__cache_exists[first_char] = FinderN2p().exists

        if first_char == 'q':
            from dbpedia_ent.dto.ent.n2.q import FinderN2q
            self.__cache_exists[first_char] = FinderN2q().exists

        if first_char == 'r':
            from dbpedia_ent.dto.ent.n2.r import FinderN2r
            self.__cache_exists[first_char] = FinderN2r().exists

        if first_char == 's':
            from dbpedia_ent.dto.ent.n2.s import FinderN2s
            self.__cache_exists[first_char] = FinderN2s().exists

        if first_char == 't':
            from dbpedia_ent.dto.ent.n2.t import FinderN2t
            self.__cache_exists[first_char] = FinderN2t().exists

        if first_char == 'u':
            from dbpedia_ent.dto.ent.n2.u import FinderN2u
            self.__cache_exists[first_char] = FinderN2u().exists

        if first_char == 'v':
            from dbpedia_ent.dto.ent.n2.v import FinderN2v
            self.__cache_exists[first_char] = FinderN2v().exists

        if first_char == 'w':
            from dbpedia_ent.dto.ent.n2.w import FinderN2w
            self.__cache_exists[first_char] = FinderN2w().exists

        if first_char == 'x':
            from dbpedia_ent.dto.ent.n2.x import FinderN2x
            self.__cache_exists[first_char] = FinderN2x().exists

        if first_char == 'y':
            from dbpedia_ent.dto.ent.n2.y import FinderN2y
            self.__cache_exists[first_char] = FinderN2y().exists

        if first_char == 'z':
            from dbpedia_ent.dto.ent.n2.z import FinderN2z
            self.__cache_exists[first_char] = FinderN2z().exists

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
        finder_cb = self._get_finder(input_text[0])
        if finder_cb:
            return finder_cb(input_text)
