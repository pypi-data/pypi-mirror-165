# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Facade to find Dictionaries on Disk """


from baseblock import BaseObject


class FindDictionaries(BaseObject):
    """ Facade to find Dictionaries on Disk """

    def __init__(self):
        """
        Created:
            25-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def hyphens() -> dict:
        from fast_sentence_tokenize.datablock.dto import d_hyphens
        return d_hyphens

    @staticmethod
    def currency() -> dict:
        from fast_sentence_tokenize.datablock.dto import d_currency
        return d_currency

    @staticmethod
    def squotes() -> dict:
        from fast_sentence_tokenize.datablock.dto import squotes
        return squotes

    @staticmethod
    def dquotes() -> dict:
        from fast_sentence_tokenize.datablock.dto import dquotes
        return dquotes

    @staticmethod
    def enclitics() -> dict:
        from fast_sentence_tokenize.datablock.dto import d_enclictics
        return d_enclictics

    @staticmethod
    def abbreviations() -> dict:
        from fast_sentence_tokenize.datablock.dto import d_abbreviations
        return d_abbreviations
