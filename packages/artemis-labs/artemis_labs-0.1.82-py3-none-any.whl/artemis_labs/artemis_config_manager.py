'''
This module stores custom config functions assigned to decorators.
It also allows retreiving this functions based on their component name
'''

# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=no-self-argument

import typing

class ArtemisConfigManager:
    '''
    This class stores custom config functions assigned to decorators.
    It also allows retreiving this functions based on their component name
    '''

    # Custom config functions
    functions = {}

    def register_function(function_name : typing.Callable, component_type : str) -> None:
        '''
        Allows user to register a callback function for a component type
        :param component_type: Component type to bind callback to
        :return: None
        '''
        ArtemisConfigManager.functions[component_type] = function_name

    def get_function(component_type : str) -> typing.Callable:
        '''
        Queries callback function associated with component_type
        :return:
        '''
        return ArtemisConfigManager.functions[component_type]
