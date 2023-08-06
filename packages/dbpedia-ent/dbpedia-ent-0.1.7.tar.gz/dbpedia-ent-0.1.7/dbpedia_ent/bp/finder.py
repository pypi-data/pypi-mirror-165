
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from typing import Callable


class Finder(object):

    __cache_exists = {}
    __cache_finder = {}
    __cache_canon = {}

    def _find_canon(self,
                    input_text: str) -> Callable:

        gram_level = input_text.count('_')

        if gram_level in self.__cache_canon:
            return self.__cache_canon[gram_level]

        elif gram_level == 0:
            from dbpedia_ent.svc import SynFinderN1
            self.__cache_canon[gram_level] = SynFinderN1().find_canon

        elif gram_level == 1:
            from dbpedia_ent.svc import SynFinderN2
            self.__cache_canon[gram_level] = SynFinderN2().find_canon

        elif gram_level == 2:
            from dbpedia_ent.svc import SynFinderN3
            self.__cache_canon[gram_level] = SynFinderN3().find_canon

        elif gram_level > 2:
            raise NotImplementedError(gram_level)

        return self.__cache_canon[gram_level]

    def _get_finder(self,
                    input_text: str) -> Callable:

        gram_level = input_text.count('_')

        if gram_level in self.__cache_finder:
            return self.__cache_finder[gram_level]

        elif gram_level == 0:
            from dbpedia_ent.svc import EntFinderN1
            self.__cache_finder[gram_level] = EntFinderN1().find

        elif gram_level == 1:
            from dbpedia_ent.svc import EntFinderN2
            self.__cache_finder[gram_level] = EntFinderN2().find

        elif gram_level == 2:
            from dbpedia_ent.svc import EntFinderN3
            self.__cache_finder[gram_level] = EntFinderN3().find

        elif gram_level > 2:
            raise NotImplementedError(gram_level)

        return self.__cache_finder[gram_level]

    def _get_exists(self,
                    input_text: str) -> Callable:

        gram_level = input_text.count('_')

        if gram_level in self.__cache_exists:
            return self.__cache_exists[gram_level]

        elif gram_level == 0:
            from dbpedia_ent.svc import EntFinderN1
            self.__cache_exists[gram_level] = EntFinderN1().exists

        elif gram_level == 1:
            from dbpedia_ent.svc import EntFinderN2
            self.__cache_exists[gram_level] = EntFinderN2().exists

        elif gram_level == 2:
            from dbpedia_ent.svc import EntFinderN3
            self.__cache_exists[gram_level] = EntFinderN3().exists

        elif gram_level > 2:
            raise NotImplementedError(gram_level)

        return self.__cache_exists[gram_level]

    @staticmethod
    def _cleanse(input_text: str) -> str:
        return input_text.lower().replace(' ', '_')

    def exists(self,
               input_text: str) -> bool:
        input_text = self._cleanse(input_text)
        finder = self._get_exists(input_text)
        return finder(input_text)

    def find(self,
             input_text: str) -> bool:
        input_text = self._cleanse(input_text)
        finder = self._get_finder(input_text)
        return finder(input_text)

    def find_canon(self,
                   input_text: str) -> bool:
        input_text = self._cleanse(input_text)
        finder = self._find_canon(input_text)
        return finder(input_text)
