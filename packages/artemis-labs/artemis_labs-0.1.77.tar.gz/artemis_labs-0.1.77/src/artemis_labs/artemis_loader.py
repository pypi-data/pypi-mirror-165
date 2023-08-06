'''
This loads in an Artemis script and generates the artemis version of this script
'''

#pylint: disable=line-too-long
#pylint: disable=anomalous-backslash-in-string
#pylint: disable=consider-using-with
#pylint: disable=too-few-public-methods


from .artemis_line_transformer import LineTransformer

class ArtemisLoader:
    '''
    This class features a single static method process_script which reads in an Artemis script
    and writes the processed version to file
    '''
    @staticmethod
    def process_script(runner_path, launch_command, code_path, dev=False, launch=True):
        '''
        This function turns a script into the Artemis version and writes it to file
        :param runner_path:
        :param launch_command:
        :param code_path:
        :param dev:
        :param launch:
        :return:
        '''

        # Read contents of decorated.py
        original_contents = open(code_path, encoding='utf-8').read()
        original_contents_lines = original_contents.split('\n')

        if dev:
            original_contents_lines.insert(0, f'app = Artemis("{runner_path}", "{launch_command}", "{code_path}", {launch}, {dev})')
            original_contents_lines.insert(0, 'atexit.register(waiter)')
            original_contents_lines.insert(0, '\t\tsleep(1)')
            original_contents_lines.insert(0, '\twhile True:')
            original_contents_lines.insert(0, 'def waiter():')
            original_contents_lines.insert(0, 'import atexit')
            original_contents_lines.insert(0, 'from artemis_labs.artemis_tester import Artemis')
            original_contents_lines.insert(0, 'sys.path.append(\'./artemis_labs/src/\')')
            original_contents_lines.insert(0, 'import sys')
            original_contents_lines.insert(0, 'from time import sleep')
        else:
            original_contents_lines.insert(0, f'app = Artemis("{runner_path}", "{launch_command}", "{code_path}", {launch}, {dev})')
            original_contents_lines.insert(0, 'atexit.register(waiter)')
            original_contents_lines.insert(0, '\t\tsleep(1)')
            original_contents_lines.insert(0, '\twhile True:')
            original_contents_lines.insert(0, 'def waiter():')
            original_contents_lines.insert(0, 'import atexit')
            original_contents_lines.insert(0, 'from artemis_labs.artemis import Artemis')
            original_contents_lines.insert(0, 'from time import sleep')


        # Transform lines
        transformed_contents_lines = LineTransformer.transform_script(original_contents_lines, dev=dev)

        # Dump back to file
        new_path = code_path.strip()[:-3] + '_artemis.py'
        out_path = new_path
        with open(out_path, 'w', encoding='utf-8') as file:
            for line in transformed_contents_lines:
                file.write(line + '\n')
        return new_path
