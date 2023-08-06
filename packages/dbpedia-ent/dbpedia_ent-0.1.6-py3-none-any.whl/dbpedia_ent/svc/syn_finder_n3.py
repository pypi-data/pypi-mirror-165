
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import Callable


class SynFinderN3(object):

    __cache_finder = {}

    def _find_canon(self,
                    first_char: str) -> Callable:

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

        if first_char == 'a':
            from dbpedia_ent.dto.syn.n3.a import FinderN3a
            self.__cache_finder[first_char] = FinderN3a().find_canon

        if first_char == 'b':
            from dbpedia_ent.dto.syn.n3.b import FinderN3b
            self.__cache_finder[first_char] = FinderN3b().find_canon

        if first_char == 'c':
            from dbpedia_ent.dto.syn.n3.c import FinderN3c
            self.__cache_finder[first_char] = FinderN3c().find_canon

        if first_char == 'd':
            from dbpedia_ent.dto.syn.n3.d import FinderN3d
            self.__cache_finder[first_char] = FinderN3d().find_canon

        if first_char == 'e':
            from dbpedia_ent.dto.syn.n3.e import FinderN3e
            self.__cache_finder[first_char] = FinderN3e().find_canon

        if first_char == 'f':
            from dbpedia_ent.dto.syn.n3.f import FinderN3f
            self.__cache_finder[first_char] = FinderN3f().find_canon

        if first_char == 'g':
            from dbpedia_ent.dto.syn.n3.g import FinderN3g
            self.__cache_finder[first_char] = FinderN3g().find_canon

        if first_char == 'h':
            from dbpedia_ent.dto.syn.n3.h import FinderN3h
            self.__cache_finder[first_char] = FinderN3h().find_canon

        if first_char == 'i':
            from dbpedia_ent.dto.syn.n3.i import FinderN3i
            self.__cache_finder[first_char] = FinderN3i().find_canon

        if first_char == 'j':
            from dbpedia_ent.dto.syn.n3.j import FinderN3j
            self.__cache_finder[first_char] = FinderN3j().find_canon

        if first_char == 'k':
            from dbpedia_ent.dto.syn.n3.k import FinderN3k
            self.__cache_finder[first_char] = FinderN3k().find_canon

        if first_char == 'l':
            from dbpedia_ent.dto.syn.n3.l import FinderN3l
            self.__cache_finder[first_char] = FinderN3l().find_canon

        if first_char == 'm':
            from dbpedia_ent.dto.syn.n3.m import FinderN3m
            self.__cache_finder[first_char] = FinderN3m().find_canon

        if first_char == 'n':
            from dbpedia_ent.dto.syn.n3.n import FinderN3n
            self.__cache_finder[first_char] = FinderN3n().find_canon

        if first_char == 'o':
            from dbpedia_ent.dto.syn.n3.o import FinderN3o
            self.__cache_finder[first_char] = FinderN3o().find_canon

        if first_char == 'p':
            from dbpedia_ent.dto.syn.n3.p import FinderN3p
            self.__cache_finder[first_char] = FinderN3p().find_canon

        if first_char == 'q':
            from dbpedia_ent.dto.syn.n3.q import FinderN3q
            self.__cache_finder[first_char] = FinderN3q().find_canon

        if first_char == 'r':
            from dbpedia_ent.dto.syn.n3.r import FinderN3r
            self.__cache_finder[first_char] = FinderN3r().find_canon

        if first_char == 's':
            from dbpedia_ent.dto.syn.n3.s import FinderN3s
            self.__cache_finder[first_char] = FinderN3s().find_canon

        if first_char == 't':
            from dbpedia_ent.dto.syn.n3.t import FinderN3t
            self.__cache_finder[first_char] = FinderN3t().find_canon

        if first_char == 'u':
            from dbpedia_ent.dto.syn.n3.u import FinderN3u
            self.__cache_finder[first_char] = FinderN3u().find_canon

        if first_char == 'v':
            from dbpedia_ent.dto.syn.n3.v import FinderN3v
            self.__cache_finder[first_char] = FinderN3v().find_canon

        if first_char == 'w':
            from dbpedia_ent.dto.syn.n3.w import FinderN3w
            self.__cache_finder[first_char] = FinderN3w().find_canon

        if first_char == 'x':
            from dbpedia_ent.dto.syn.n3.x import FinderN3x
            self.__cache_finder[first_char] = FinderN3x().find_canon

        if first_char == 'y':
            from dbpedia_ent.dto.syn.n3.y import FinderN3y
            self.__cache_finder[first_char] = FinderN3y().find_canon

        if first_char == 'z':
            from dbpedia_ent.dto.syn.n3.z import FinderN3z
            self.__cache_finder[first_char] = FinderN3z().find_canon

        if first_char in self.__cache_finder:
            return self.__cache_finder[first_char]

    def find_canon(self,
                   input_text: str) -> bool:

        input_text = input_text.lower()
        exists_cb = self._find_canon(input_text[0])
        if exists_cb:
            return exists_cb(input_text)
