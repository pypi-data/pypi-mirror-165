'''
This parses lines into lists of tokens called a TokenChain
'''

#pylint: disable=line-too-long
#pylint: disable=anomalous-backslash-in-string

from typing import Any, List

from .artemis_token_parser import TokenParser
from .artemis_token import Token, TokenType

class TokenChain():
    '''
    This represents a chain of tokens associated with a line
    '''

    def __init__(self, line : str):
        '''
        This takes in a line and turns it into a token chain using the TokenParser
        :param line: Line that will be used to generate the token chain
        '''

        old_line = line
        line = line.strip()
        self.is_token_chain = False
        self.tokens = []
        if len(line) == 0 or line[0] != '#':
            return
        self.indentation, self.tokens = TokenParser.parse_line(old_line)

    def get_indentation(self) -> str:
        '''
        Gets the indentation of the line / token chain
        :return Indentiation of line
        '''
        return self.indentation

    def get_tokens_str(self) -> str:
        '''
        Creates a comma-separated list of the stringified tokens in the token chain
        :return Stringified comma-separated list of tokens
        '''

        if not self.is_valid():
            return "[Invalid token chain]"
        out = '['
        for token in self.tokens[:-1]:
            out += str(token) + ', '
        if len(self.tokens) > 0:
            out += str(self.tokens[-1])
        out += ']'
        return out

    def __str__(self) -> str:
        '''
        Turns the token chain into a string
        :return Stringified version of token chain
        '''
        out = 'Token' + '\n\tCommand: ' + self.get_command() + '\n'
        out += '\tComponent Type: ' + self.get_component_type() + '\n'
        out += "\tTokens: " + self.get_tokens_str() + "\n"
        out +=  '\tTags: ' + "\n"
        for tag in self.get_tags():
            out += "\t" + tag + "\n"
        out += '\tArgs' + "\n"
        for arg in self.get_args():
            out += "\t" + arg + "\n"
        return out


    def is_valid(self) -> bool:
        '''
        Checks if the token chain is valid
        :return If the token chain is valid
        '''

        # Verify tokens exist
        if len(self.tokens) == 0:
            return False

        # Verify command exists
        if self.tokens[0].token_type != TokenType.COMMAND:
            return False

        # We dont need to verify compnent type if we're just enabling or disabling
        single_command_tokens = ['@flag', '@doc', '@blockdoc', '@marker', '@linkedcode' ,'@stop', '@card', '@samecard']
        if self.tokens[0].token_value in single_command_tokens:
            return True

        # Verify component type provided
        if len(self.tokens) <= 1:
            return False

        # Verify component type exists
        if self.tokens[1].token_type != TokenType.COMPONENT_TYPE:
            return False
        return True


    def get_tags(self) -> List[Token]:
        '''
        Gets all Tokens that are tags in the token chain
        :return List of tag tokens in token chain
        '''

        tags = []
        for token in self.tokens:
            if token.token_type == TokenType.TAG:
                tags.append(token.token_value)
        return tags

    def get_named_args(self) -> List[Token]:
        '''
        Gets all Tokens that are named args in the token chain
        :return List of named args tokens in token chain
        '''

        named_args = []
        for token in self.tokens:
            if token.token_type == TokenType.NAMED_ARGUMENT:
                named_args.append(token.token_value)
        return named_args

    def get_args(self) -> List[Token]:
        '''
        Gets all Tokens that are args in the token chain
        :return List of args tokens in token chain
        '''

        args = []
        for token in self.tokens:
            if token.token_type == TokenType.ARGUMENT:
                args.append(token.token_value)
        return args

    def get_command(self) -> str:
        '''
        Gets the value of the command in the token chain or None if one is not found
        :return Value of command token in token chain
        '''
        if len(self.tokens) == 0:
            return None
        if self.tokens[0].token_type == TokenType.COMMAND:
            return self.tokens[0].token_value
        return ""

    def get_component_type(self) -> str:
        '''
        Get the value of the component type in the token chain or None if not found
        :return Value of component type in token chain
        '''
        if self.tokens[1].token_type == TokenType.COMPONENT_TYPE:
            return self.tokens[1].token_value
        return ""

    def get_component_value(self) -> Any:
        '''
        Get the value of the value token in the token chain or None if not found
        :return Value of value token in token chain
        '''
        if self.tokens[2].token_type == TokenType.VALUE:
            return self.tokens[2].token_value
        return None
