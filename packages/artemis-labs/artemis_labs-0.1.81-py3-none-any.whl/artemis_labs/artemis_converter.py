'''
This module is used to convert different types between one another
'''

# pylint: disable=line-too-long
# pylint: disable=wildcard-import
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods

from typing import Dict, List, Any
import numpy as np

class ArtemisConverter:

    '''
    Output Processing
    '''
    @staticmethod
    def _convert_dict_to_list(dict_to_convert : Dict) -> List:
        '''
        This converts a dictionary into a list of nested key-value pairs
        :param value: Dictionary to turn into list
        :return: List form of dictionary
        '''

        # Validate input
        assert isinstance(dict_to_convert, dict)

        # Turn dictionary into nested key-value lists
        dict_list = []
        for key, value in dict_to_convert.items():
            dict_list.append([key, value])
        return dict_list

    @staticmethod
    def _convert_list_to_string_list(list_to_convert : list) -> str:
        '''
        This converts a list into a serialized string form
        :param value: List to serialize
        :return: Serialized string form of value
        '''

        # Validate input
        assert isinstance(list_to_convert, list)

        # Change to numpy array
        arr = np.array(list_to_convert)

        # Change shape
        if len(arr.shape) == 1:
            arr = arr.reshape(arr.shape[0], 1)

        # Convert back to list
        value_list = arr.tolist()

        # Convert into string form and change single quotes to double quotes
        value_str = str(value_list)
        value_str = value_str.replace("'", '"')
        return value_str

    @staticmethod
    def _convert_np_array_to_string_list(np_array_to_convert : np.ndarray) -> str:
        '''
        This converts a numpy array into a serialized string form
        :param value: Numpy array to serialize
        :return: Serialized string form of value
        '''
        # Nest if its 1D
        if len(np_array_to_convert.shape) == 1:
            value = np_array_to_convert.reshape(np_array_to_convert.shape[0], 1)
        else:
            value = np_array_to_convert

        # Convert to list and use list function
        list_value = list(value)
        return ArtemisConverter._convert_list_to_string_list(list_value)


    @staticmethod
    def convert_type(value_to_convert : Any, component_type : str) -> Any:
        '''
        This automatically converts value to a serialized type
        based on componentType and the type of value
        :param component_type: Type of component we're converting
        :return: Serialized output
        '''
        # Unique Types
        table_types = ['table']

        # Process as distinct if statements
        if isinstance(value_to_convert, dict):
            value_to_convert = ArtemisConverter._convert_dict_to_list(value_to_convert)

        if isinstance(value_to_convert, range):
            value_to_convert = list(value_to_convert)

        if isinstance(value_to_convert, list) and component_type in table_types:
            value_to_convert = ArtemisConverter._convert_list_to_string_list(value_to_convert)

        if isinstance(value_to_convert, np.ndarray) and component_type in table_types:
            value_to_convert = ArtemisConverter._convert_np_array_to_string_list(value_to_convert)

        return value_to_convert
