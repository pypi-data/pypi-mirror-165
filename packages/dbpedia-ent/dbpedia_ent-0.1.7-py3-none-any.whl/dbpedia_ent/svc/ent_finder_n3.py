
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import Callable


class EntFinderN3(object):

    __cache_exists = {}
    __cache_finder = {}

    def _get_finder(self,
                    first_char: str) -> Callable:

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

        if first_char == 'a':
            from dbpedia_ent.dto.ent.n3.a import FinderN3a
            self.__cache_finder[first_char] = FinderN3a().find

        if first_char == 'b':
            from dbpedia_ent.dto.ent.n3.b import FinderN3b
            self.__cache_finder[first_char] = FinderN3b().find

        if first_char == 'c':
            from dbpedia_ent.dto.ent.n3.c import FinderN3c
            self.__cache_finder[first_char] = FinderN3c().find

        if first_char == 'd':
            from dbpedia_ent.dto.ent.n3.d import FinderN3d
            self.__cache_finder[first_char] = FinderN3d().find

        if first_char == 'e':
            from dbpedia_ent.dto.ent.n3.e import FinderN3e
            self.__cache_finder[first_char] = FinderN3e().find

        if first_char == 'f':
            from dbpedia_ent.dto.ent.n3.f import FinderN3f
            self.__cache_finder[first_char] = FinderN3f().find

        if first_char == 'g':
            from dbpedia_ent.dto.ent.n3.g import FinderN3g
            self.__cache_finder[first_char] = FinderN3g().find

        if first_char == 'h':
            from dbpedia_ent.dto.ent.n3.h import FinderN3h
            self.__cache_finder[first_char] = FinderN3h().find

        if first_char == 'i':
            from dbpedia_ent.dto.ent.n3.i import FinderN3i
            self.__cache_finder[first_char] = FinderN3i().find

        if first_char == 'j':
            from dbpedia_ent.dto.ent.n3.j import FinderN3j
            self.__cache_finder[first_char] = FinderN3j().find

        if first_char == 'k':
            from dbpedia_ent.dto.ent.n3.k import FinderN3k
            self.__cache_finder[first_char] = FinderN3k().find

        if first_char == 'l':
            from dbpedia_ent.dto.ent.n3.l import FinderN3l
            self.__cache_finder[first_char] = FinderN3l().find

        if first_char == 'm':
            from dbpedia_ent.dto.ent.n3.m import FinderN3m
            self.__cache_finder[first_char] = FinderN3m().find

        if first_char == 'n':
            from dbpedia_ent.dto.ent.n3.n import FinderN3n
            self.__cache_finder[first_char] = FinderN3n().find

        if first_char == 'o':
            from dbpedia_ent.dto.ent.n3.o import FinderN3o
            self.__cache_finder[first_char] = FinderN3o().find

        if first_char == 'p':
            from dbpedia_ent.dto.ent.n3.p import FinderN3p
            self.__cache_finder[first_char] = FinderN3p().find

        if first_char == 'q':
            from dbpedia_ent.dto.ent.n3.q import FinderN3q
            self.__cache_finder[first_char] = FinderN3q().find

        if first_char == 'r':
            from dbpedia_ent.dto.ent.n3.r import FinderN3r
            self.__cache_finder[first_char] = FinderN3r().find

        if first_char == 's':
            from dbpedia_ent.dto.ent.n3.s import FinderN3s
            self.__cache_finder[first_char] = FinderN3s().find

        if first_char == 't':
            from dbpedia_ent.dto.ent.n3.t import FinderN3t
            self.__cache_finder[first_char] = FinderN3t().find

        if first_char == 'u':
            from dbpedia_ent.dto.ent.n3.u import FinderN3u
            self.__cache_finder[first_char] = FinderN3u().find

        if first_char == 'v':
            from dbpedia_ent.dto.ent.n3.v import FinderN3v
            self.__cache_finder[first_char] = FinderN3v().find

        if first_char == 'w':
            from dbpedia_ent.dto.ent.n3.w import FinderN3w
            self.__cache_finder[first_char] = FinderN3w().find

        if first_char == 'x':
            from dbpedia_ent.dto.ent.n3.x import FinderN3x
            self.__cache_finder[first_char] = FinderN3x().find

        if first_char == 'y':
            from dbpedia_ent.dto.ent.n3.y import FinderN3y
            self.__cache_finder[first_char] = FinderN3y().find

        if first_char == 'z':
            from dbpedia_ent.dto.ent.n3.z import FinderN3z
            self.__cache_finder[first_char] = FinderN3z().find

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

    def _get_exists(self,
                    first_char: str) -> Callable:

        if first_char in self.__cache_exists:
            return self.__cache_exists[first_char]

        if first_char == 'a':
            from dbpedia_ent.dto.ent.n3.a import FinderN3a
            self.__cache_exists[first_char] = FinderN3a().exists

        if first_char == 'b':
            from dbpedia_ent.dto.ent.n3.b import FinderN3b
            self.__cache_exists[first_char] = FinderN3b().exists

        if first_char == 'c':
            from dbpedia_ent.dto.ent.n3.c import FinderN3c
            self.__cache_exists[first_char] = FinderN3c().exists

        if first_char == 'd':
            from dbpedia_ent.dto.ent.n3.d import FinderN3d
            self.__cache_exists[first_char] = FinderN3d().exists

        if first_char == 'e':
            from dbpedia_ent.dto.ent.n3.e import FinderN3e
            self.__cache_exists[first_char] = FinderN3e().exists

        if first_char == 'f':
            from dbpedia_ent.dto.ent.n3.f import FinderN3f
            self.__cache_exists[first_char] = FinderN3f().exists

        if first_char == 'g':
            from dbpedia_ent.dto.ent.n3.g import FinderN3g
            self.__cache_exists[first_char] = FinderN3g().exists

        if first_char == 'h':
            from dbpedia_ent.dto.ent.n3.h import FinderN3h
            self.__cache_exists[first_char] = FinderN3h().exists

        if first_char == 'i':
            from dbpedia_ent.dto.ent.n3.i import FinderN3i
            self.__cache_exists[first_char] = FinderN3i().exists

        if first_char == 'j':
            from dbpedia_ent.dto.ent.n3.j import FinderN3j
            self.__cache_exists[first_char] = FinderN3j().exists

        if first_char == 'k':
            from dbpedia_ent.dto.ent.n3.k import FinderN3k
            self.__cache_exists[first_char] = FinderN3k().exists

        if first_char == 'l':
            from dbpedia_ent.dto.ent.n3.l import FinderN3l
            self.__cache_exists[first_char] = FinderN3l().exists

        if first_char == 'm':
            from dbpedia_ent.dto.ent.n3.m import FinderN3m
            self.__cache_exists[first_char] = FinderN3m().exists

        if first_char == 'n':
            from dbpedia_ent.dto.ent.n3.n import FinderN3n
            self.__cache_exists[first_char] = FinderN3n().exists

        if first_char == 'o':
            from dbpedia_ent.dto.ent.n3.o import FinderN3o
            self.__cache_exists[first_char] = FinderN3o().exists

        if first_char == 'p':
            from dbpedia_ent.dto.ent.n3.p import FinderN3p
            self.__cache_exists[first_char] = FinderN3p().exists

        if first_char == 'q':
            from dbpedia_ent.dto.ent.n3.q import FinderN3q
            self.__cache_exists[first_char] = FinderN3q().exists

        if first_char == 'r':
            from dbpedia_ent.dto.ent.n3.r import FinderN3r
            self.__cache_exists[first_char] = FinderN3r().exists

        if first_char == 's':
            from dbpedia_ent.dto.ent.n3.s import FinderN3s
            self.__cache_exists[first_char] = FinderN3s().exists

        if first_char == 't':
            from dbpedia_ent.dto.ent.n3.t import FinderN3t
            self.__cache_exists[first_char] = FinderN3t().exists

        if first_char == 'u':
            from dbpedia_ent.dto.ent.n3.u import FinderN3u
            self.__cache_exists[first_char] = FinderN3u().exists

        if first_char == 'v':
            from dbpedia_ent.dto.ent.n3.v import FinderN3v
            self.__cache_exists[first_char] = FinderN3v().exists

        if first_char == 'w':
            from dbpedia_ent.dto.ent.n3.w import FinderN3w
            self.__cache_exists[first_char] = FinderN3w().exists

        if first_char == 'x':
            from dbpedia_ent.dto.ent.n3.x import FinderN3x
            self.__cache_exists[first_char] = FinderN3x().exists

        if first_char == 'y':
            from dbpedia_ent.dto.ent.n3.y import FinderN3y
            self.__cache_exists[first_char] = FinderN3y().exists

        if first_char == 'z':
            from dbpedia_ent.dto.ent.n3.z import FinderN3z
            self.__cache_exists[first_char] = FinderN3z().exists

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
