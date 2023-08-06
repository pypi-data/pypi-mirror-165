#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import unicodedata2
from typing import Callable


def text_to_chars(input_text: str) -> str:

    def transform(ch):
        """Checks whether `char` is a punctuation character."""
        if ch.isnumeric():
            return '_'
        cp = ord(ch)
        if (cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126):
            return '_'  # is punct
        cat = unicodedata2.category(ch)
        if cat.startswith("P"):
            return '_'  # is punct
        return ch  # not punct

    input_text = [transform(ch) for ch in input_text]

    return input_text


def ngram_exists(input_text: str,
                 d_trie_finder: Callable) -> bool:

    input_text = input_text.lower().replace(' ', '_')
    input_text = input_text.replace('_&_', '_and_')

    chars = text_to_chars(input_text[:3])

    d_trie = d_trie_finder(''.join(chars[:2]))
    if d_trie and chars[2] in d_trie:
        return input_text in d_trie[chars[2]]

    return False


def ngram_finder(input_text: str,
                 d_trie_finder: Callable) -> list or None:

    input_text = input_text.lower().replace(' ', '_')
    input_text = input_text.replace('_&_', '_and_')

    chars = text_to_chars(input_text[:3])

    d_trie = d_trie_finder(''.join(chars[:2]))
    if d_trie and chars[2] in d_trie:
        return d_trie[chars[2]]


def find_canon(input_text: str,
               d_trie_finder: Callable) -> bool:

    input_text = input_text.lower().replace(' ', '_')
    chars = text_to_chars(input_text[:2])

    d_trie = d_trie_finder(''.join(chars[:2]))
    if d_trie and input_text in d_trie:
        return d_trie[input_text]

    return input_text
