#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Use spaCy to Parse Input Tokens """


from baseblock import Stopwatch
from baseblock import BaseObject


from spacy_token_parser.dmo import GrafflParserSpacy
from spacy_token_parser.dmo import GrafflParserWordnet
from spacy_token_parser.dmo import GrafflParserNormalize
from spacy_token_parser.dmo import GrafflParserPunctuation
from spacy_token_parser.dmo import GrafflParserCoordinates
from spacy_token_parser.dmo import GrafflParserSquots
from spacy_token_parser.dmo import GrafflParserResultSet


class ParseInputTokens(BaseObject):
    """ Use spaCy to Parse Input Tokens """

    def __init__(self):
        """ Change Log

        Created:
            1-Oct-2021
            craigtrim@gmail.com
        Updated:
            13-Oct-2021
            craigtrim@gmail.com
            *   refactored into component parts in pursuit of
                https://github.com/grafflr/graffl-core/issues/41
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                tokens: list) -> list:

        sw = Stopwatch()

        tokens = GrafflParserSquots().process(tokens)
        doc = GrafflParserSpacy().process(' '.join(tokens))

        results = GrafflParserResultSet().process(doc)
        results = GrafflParserPunctuation().process(results)
        results = GrafflParserNormalize().process(results)
        results = GrafflParserCoordinates().process(results)
        results = GrafflParserWordnet().process(results)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Input Token Parsing Completed",
                f"\tTotal Tokens: {len(results)}",
                f"\tTotal Time: {str(sw)}"]))

        return results, doc
