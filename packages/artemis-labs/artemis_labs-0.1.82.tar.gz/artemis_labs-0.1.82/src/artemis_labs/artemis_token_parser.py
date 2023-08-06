'''
This module contains code related to parsing lines into tokens
'''

# pylint: disable=line-too-long
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-boolean-expressions
# pylint: disable=too-many-boolean-expressions
# pylint: disable=too-many-locals
import re
from typing import List
from .artemis_token import TokenType, Token

class TokenParser():
    '''
    This class is used to parse lines and text into tokens
    '''
    @staticmethod
    def parse_line(line) -> str:
        '''
        This parses a line into a list of tokens
        :param line: String line read in from file
        :return: List of parsed tokens
        '''

        # Store old line
        old_line = line

        # Clean line
        line = line.strip()

        # Remove trailing escape
        if line.endswith('\\'):
            line = line[:-1]

        # Remove lone escape
        line = line.replace(' \\ ', '')

        # Verify comment
        if not line.startswith('#'):
            return ('', [])

        # Strip comment
        line = line[1:].strip()

        # Tokenize
        try:
            tokens = TokenParser.tokenify_line(line)
        except Exception as exception:
            print("[Artemis] Error: Failed to tokenify line")
            print(exception)
            return ('', [])

        # Remove empty tokens
        tokens = [token for token in tokens if token.strip() != '']

        # Check to make sure its non-empty
        if tokens is None or len(tokens) == 0:
            return ('', [])

        # Parse first token
        first_token = TokenParser.parse_token(tokens[0])

        # Exit if first token is not valid
        valid_tokens = ['@doc', '@input', '@flag', '@output', '@blockdoc', '@marker', '@linkedcode', '@stop', '@card']
        if first_token.token_value not in valid_tokens:
            return ('', [])

        # Ensure inputs and outputs specifiy type
        if first_token.token_value == '@doc':

            # Get markdown content
            doc_content = line[line.find('@doc') + len('@doc'):].strip()
            component_type = 'markdown'

            # Ensure value
            if doc_content.strip() == '':
                return ('', [])

            # Process doc token
            parsed_tokens = [TokenParser.parse_token('@doc'), Token(TokenType.COMPONENT_TYPE, component_type), Token(TokenType.VALUE, doc_content.strip())]

        elif tokens[0].strip() == '@marker':

            # Get marker name
            marker_name = line[line.find('@marker') + len('@marker'):].strip()
            if marker_name == '':
                return ('', [])

            # Tokenify marker name
            marker_name_tokens = TokenParser.tokenify_line(marker_name)
            if len(marker_name_tokens) == 0:
                return ('', [])

            # Process marker token
            parsed_tokens = [TokenParser.parse_token('@marker'), Token(TokenType.COMPONENT_TYPE, marker_name_tokens[0].strip())]
        else:

            # Tokenize line
            parsed_tokens = [TokenParser.parse_token(token) for token in tokens]

            # Mark any component types other than the first errors
            found_first_component_type = False
            for i, parsed_token in enumerate(parsed_tokens):
                if parsed_token.token_type == TokenType.COMPONENT_TYPE:
                    if not found_first_component_type:
                        found_first_component_type = True
                    else:
                        parsed_tokens[i].token_type = TokenType.ERROR # pylint: disable=unnecessary-list-index-lookup

            # Prune error tokens
            parsed_tokens = [parsed_token for parsed_token in parsed_tokens if parsed_token.token_type != TokenType.ERROR]

            # Ensure first token is a command
            if first_token.token_type != TokenType.COMMAND:
                return ('', [])

            # Check token count
            two_token_types = ['@input', '@output']
            if first_token.token_value in two_token_types and len(parsed_tokens) < 2:
                has_data_named_args = False
                for parsed_token in parsed_tokens:
                    if parsed_token.token_type == TokenType.NAMED_ARGUMENT and parsed_token.token_value[0] == 'data':
                        has_data_named_args = True
                if not has_data_named_args:
                    return ('', [])

            # Ensure input and output have component type
            if first_token.token_value in two_token_types and parsed_tokens[1].token_type != TokenType.COMPONENT_TYPE:
                return ('', [])

            # Ensure proper command count
            command_count = 0
            for parsed_token in parsed_tokens:
                if parsed_token.token_type == TokenType.COMMAND:
                    command_count += 1
            if command_count == 0 or command_count > 1:
                return ('', [])

            # Validate token count
            two_token_types = ['@input', '@output']
            if first_token.token_value in two_token_types and len(parsed_tokens) < 2:
                return ('', [])

            # Trim garbage for blockdoc
            single_token_types = ['@blockdoc']
            if first_token.token_value in single_token_types:
                parsed_tokens = [first_token]

            # Validate flag
            if first_token.token_value == '@flag':

                # Validate inputs
                if len(parsed_tokens) < 2 or parsed_tokens[1].token_type != TokenType.ARGUMENT:
                    return ('', [])

                # Ensure only one arg
                arg_counter = 0
                for parsed_token in parsed_tokens:
                    if parsed_token.token_type == TokenType.ARGUMENT:
                        arg_counter += 1
                if arg_counter != 1:
                    return ('', [])

                # Remove erroneous tokens
                clean_parsed_tokens = []
                for parsed_token in parsed_tokens:
                    valid_token_types = [TokenType.COMMAND, TokenType.ARGUMENT, TokenType.TAG]
                    if parsed_token.token_type in valid_token_types:
                        clean_parsed_tokens.append(parsed_token)
                parsed_tokens = clean_parsed_tokens

            # Validate linked code
            if first_token.token_value == '@linkedcode':

                # Validate we have start and end
                found_start = False
                found_end = False
                clean_parsed_tokens = [first_token]
                for parsed_token in parsed_tokens[1:]:
                    if parsed_token.token_type == TokenType.NAMED_ARGUMENT and parsed_token.token_value[0] == 'start':
                        found_start = True
                        clean_parsed_tokens.append(parsed_token)
                    if parsed_token.token_type == TokenType.NAMED_ARGUMENT and parsed_token.token_value[0] == 'end':
                        found_end = True
                        clean_parsed_tokens.append(parsed_token)
                if not found_start or not found_end:
                    return ('', [])

                # Clean args
                parsed_tokens = clean_parsed_tokens

        # Validate

        # Return with indentation
        indentation = ''
        if not old_line.startswith('#'):
            indentation = old_line[:old_line.find('#')]
        return (indentation, parsed_tokens)

    @staticmethod
    def tokenify_line(line : str) -> List[str]:
        '''
        Splits a line into tokens. This is similar to .split, but we dont split inside quotes
        :param line:
        :return: List of str tokens that the line has been split into
        '''
        tokens = []
        last_token = ""
        inside_quote = False
        inside_angle_bracket = False
        for char_val in line:
            if char_val == '<':
                inside_angle_bracket = True
            if char_val == '>':
                inside_angle_bracket = False
            if char_val == '\"':
                inside_quote = not inside_quote
            if not inside_quote and char_val == ' ' and not inside_angle_bracket:
                tokens.append(last_token)
                last_token = ''
                continue
            last_token += char_val
        if last_token != '':
            tokens.append(last_token)
        return tokens

    @staticmethod
    def parse_token(token : str) -> Token:
        '''
        This turns a string token into a parsed token
        :param token: string token
        :return:
        '''
        try:

            # Clean line and basic sanity check
            token = token.strip()
            if len(token) <= 1:
                return Token(TokenType.ERROR, token)

            # Tag Path
            if token.startswith("#"):
                if token[1] == ' ' or token.count('#') > 1 or "'" in token or "\"" in token or '\\' in token or '@' in token or '--' in token or '=' in token:
                    return Token(TokenType.ERROR, token)
                return Token(TokenType.TAG, token)

            # Command Path
            if token.startswith("@"):
                if token[1] == ' ' or token.count('@') > 1 or "'" in token or "\"" in token or '\\' in token or '=' in token:
                    return Token(TokenType.ERROR, token)
                return Token(TokenType.COMMAND, token)

            # Argument Path
            if token.startswith("--") and len(token) > 2:
                if token[2] == ' ' or token.count('-') > 2 or "'" in token or "\"" in token or '\\' in token or '=' in token:
                    return Token(TokenType.ERROR, token)
                return Token(TokenType.ARGUMENT, token[2:])

            # Named Argument Path
            if '=' in token and len(token.split('=')) == 2:

                # Get arg name and value
                arg_name = token.split('=')[0].lstrip()
                arg_val = token.split('=')[1].rstrip()

                # Skip if arg_val empty
                if len(arg_val.strip()) == 0:
                    return Token(TokenType.ERROR, '')

                # Force data arg value to be of form << ... >>
                if 'data' in arg_name:
                    if ('<<' in arg_val or '>>' in arg_val) and (not arg_val.startswith('<<') or not arg_val.endswith('>>')):
                        return Token(TokenType.ERROR, '')
                    if '<<' not in arg_val and '>>' not in arg_val:
                        arg_val = '<<' + arg_val + '>>'
                        token = arg_name + '=' + arg_val

                # Check if arg value is eval expression
                is_eval_expression = token.split('=')[1].startswith('<') and token.split('=')[1].endswith('>')

                # Error if we have \ and its not an eval expression
                if '\\' in token and not is_eval_expression:
                    return Token(TokenType.ERROR, '')

                # Get arg name and value
                arg_name = token.split('=')[0].lstrip()
                arg_val = token.split('=')[1].rstrip()

                # Ensure no weird spacing
                if arg_name.endswith(' ') or arg_val.startswith(' '):
                    return Token(TokenType.ERROR, '')

                # Ensure no special characters in the argument
                if '@' in arg_name or '#' in arg_name or '--' in arg_name:
                    return Token(TokenType.ERROR, '')

                if '@' in arg_val or '#' in arg_val or '--' in arg_val:
                    return Token(TokenType.ERROR, '')

                # Ensure non-null arg
                if len(arg_name) == 0 or len(arg_val) == 0 or '"' in token.split('=')[0] or '\'' in token.split('=')[0]:
                    return Token(TokenType.ERROR, '')

                # Handle eval code
                if is_eval_expression:
                    return Token(TokenType.NAMED_ARGUMENT, (token.split('=')[0], arg_val))

                # Clean unescaped quotes
                if arg_val.startswith("\"") and arg_val.endswith("\""):
                    arg_val = arg_val[1:-1]
                if arg_val.startswith("\""):
                    arg_val = "\\\"" + arg_val[1:]
                if arg_val.endswith("\""):
                    arg_val = arg_val[0:-1] + "\\\""
                unescaped_quotes = re.findall('[^\\\\]\"', arg_val)
                for unescaped_quote in unescaped_quotes:
                    replacement = unescaped_quote[0] + "\\\""
                    arg_val = arg_val.replace(unescaped_quote, replacement)

                # Clean unescaped single quotes
                if arg_val.startswith("\'") and arg_val.endswith("\'"):
                    arg_val = arg_val[1:-1]
                if arg_val.startswith("\'"):
                    arg_val = "\\\'" + arg_val[1:]
                if arg_val.endswith("\'"):
                    arg_val = arg_val[0:-1] + "\\\'"
                unescaped_quotes = re.findall('[^\\\\]\'', arg_val)
                for unescaped_quote in unescaped_quotes:
                    replacement = unescaped_quote[0] + "\\\'"
                    arg_val = arg_val.replace(unescaped_quote, replacement)

                # Return data arg
                return Token(TokenType.NAMED_ARGUMENT, (token.split('=')[0], arg_val))

            # Component Type Path
            if ' ' in token or '\'' in token or '\"' in token or '=' in token or '#' in token or '@' in token or '\\' in token:
                return Token(TokenType.ERROR, '')
            return Token(TokenType.COMPONENT_TYPE, token)
        except Exception as exception:
            print("[Artemis] Failed to parse " + token)
            print("Error: ")
            print(exception)
            return Token(TokenType.COMPONENT_TYPE, token)
