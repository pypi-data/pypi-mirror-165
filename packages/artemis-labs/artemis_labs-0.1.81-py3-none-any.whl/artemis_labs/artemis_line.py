'''
This module contains the Line class
'''

class Line():
    '''
    This represents a parsed line. You can use this to check if the line is a comment,
    query the lhs, rhs, and get the line
    '''
    def __init__(self, line : str):
        '''
        This strips and stores the line. This also splits the line if it has an equals,
        and it caches if the line is a comment
        :param line Line used to construct this object
        '''
        self.line = line
        strip_line = self.line.strip()

        # Iniitialize variables
        self.comment = False
        self.lhs = ''
        self.rhs = ''

        # Check if line is a comment
        if len(strip_line) == 0:
            return
        self.comment = strip_line[0] == '#'

        # Parse sides of line
        if '=' not in strip_line:
            self.lhs = strip_line.replace(';', '')
            self.rhs = ''
        else:
            try:
                self.lhs = line.split('=')[0].strip().replace(';', '')
                self.rhs = line.split('=')[1].strip()
            except Exception as exception:
                print('Failed to parse line: ' + line)
                print('Exception: ' + str(exception))
                raise exception

    def is_comment(self) -> bool:
        '''
        This returns if the line is a comment or not
        :return if the line is a comment or not
        '''
        return self.comment

    def get_lhs(self) -> str:
        '''
        This returns the lhs of the line. If there is no equals, this is the line
        :return lhs of line
        '''
        return self.lhs

    def get_rhs(self) -> str:
        '''
        This returns the rhs of the line. If there is no equals, this is the line
        :return rhs of line
        '''
        return self.rhs

    def get_line(self) -> str:
        '''
        This returns the line used to construct this
        :return line
        '''
        return self.line
