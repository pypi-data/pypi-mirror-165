from .dmo import *
from .svc import *


from .svc.parse_input_tokens import ParseInputTokens

parse = ParseInputTokens().process


def parse_tokens(tokens: list) -> list:
    return parse(tokens)
