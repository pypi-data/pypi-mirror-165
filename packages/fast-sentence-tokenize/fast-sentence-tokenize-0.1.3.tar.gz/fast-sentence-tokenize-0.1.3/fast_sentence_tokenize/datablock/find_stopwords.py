# !/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Facade to find Stopwords Data on Disk """


from baseblock import EnvIO
from baseblock import BaseObject

from fast_sentence_tokenize.datablock.dto import stopwords


class FindStopWords(BaseObject):
    """ Facade to find Stopwords Data on Disk """

    def __init__(self):
        """
        Created:
            25-Aug-2022
            craigtrim@gmail.com
            *   in pursuit of 
                https://github.com/grafflr/graffl-core/issues/120
        """
        BaseObject.__init__(self, __name__)

    def exists(self,
               input_text: str) -> bool:
        input_text = input_text.lower().strip()
        return input_text in stopwords
