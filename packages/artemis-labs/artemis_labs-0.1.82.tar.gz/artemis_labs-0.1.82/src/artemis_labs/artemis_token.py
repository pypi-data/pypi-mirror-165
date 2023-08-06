'''
This module contains code related to decorator tokens (the elements
that comprise decorators)
Examples of tokens include: '@command' '--argument' '#tag' and so on
'''

from enum import Enum


class TokenType(Enum):
    '''
    This enum represents possible Token types that can be parsed in
    Tokens comprise decorators
    '''
    COMMAND = 0
    COMPONENT_TYPE = 1
    ARGUMENT = 2
    TAG = 3
    VALUE = 4
    NAMED_ARGUMENT = 5
    UNKNOWN = 6
    ERROR = 7

class Token():
    '''
    This is the token class, which stores the type and value
    of a parsed token
    '''

    def __init__(self, token_type : TokenType, token_value : str):
        '''
        This initializes the token with the provided type and value
        :param token_type: Type of token
        :param token_value: Value of token
        '''
        self.token_type = token_type
        self.token_value = token_value

    def __str__(self) -> str:
        '''
        This converts a token to a string
        :return: String version of token
        '''
        if isinstance(self.token_value, str):
            return self.token_value
        if isinstance(self.token_value, tuple):
            return str(self.token_value)
        return str(self.token_value)

    def is_valid(self) -> bool:
        '''
        This checks if a token is valid
        :return: Whether token is valid or not
        '''
        return self.token_type == TokenType.ERROR
