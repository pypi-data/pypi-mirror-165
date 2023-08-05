#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Text Tokenization API """


from functools import lru_cache


class Tokenizer(object):
    """ Text Tokenization API """

    def __init__(self):
        self._spacy = None
        self._custom = None
        self._whitespace = None

    @lru_cache
    def spacy(self,
              input_text: str) -> list:
        """Tokenize with spaCy 

        Args:
            input_text (str): input text of any length

        Returns:
            list: list of tokens
        """
        if not self._spacy:
            from fast_sentence_tokenize.svc import TokenizeUseSpacy
            self._spacy = TokenizeUseSpacy().process

        return self._spacy(input_text)

    @lru_cache
    def whitespace(self,
                   input_text: str) -> list:
        """Tokenize using Whitespace 

        Args:
            input_text (str): input text of any length

        Returns:
            list: list of tokens
        """
        if not self._whitespace:
            from fast_sentence_tokenize.svc import TokenizeUseWhitespace
            self._whitespace = TokenizeUseWhitespace().process

        return self._whitespace(input_text)

    @lru_cache
    def input_text(self,
                   input_text: str) -> list:
        """Tokenize with Custom Tokenizer 

        Args:
            input_text (str): input text of any length

        Returns:
            list: list of tokens
        """
        if not self._custom:
            from fast_sentence_tokenize.svc import TokenizeUseGraffl
            self._custom = TokenizeUseGraffl().process

        return self._custom(input_text)
