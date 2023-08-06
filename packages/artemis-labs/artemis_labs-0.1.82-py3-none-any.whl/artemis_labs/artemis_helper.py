'''
This module contains an array of helper functions to serialize different data into
a form comaptible with the Artemis browser as well as convert data
between types
'''

#pylint: disable=line-too-long
#pylint: disable=broad-except
#pylint: disable=dangerous-default-value

import base64
import io
import inspect
from enum import Enum
from typing import Any
import traceback

import os
import matplotlib.pyplot as plt
import numpy as np


# Enum class
class ArtemisType(Enum):
    '''
    This enum represents possible types Artemis can handle.
    This is used by Artemis Helper
    '''
    MATPLOTLIB_PLOT = 1
    MATPLOTLIB_FIGURE = 2
    LIST = 3
    DICT = 4
    NUMPY_ARRAY = 5
    GLB_MODEL = 6


 # Helpers
class ArtemisHelper:
    '''
    This class contains static helper functions to convert between
    types and serialize data for Artmeis browser
    '''

    # ================================================================
    # General Functions
    # ================================================================
    @staticmethod
    def convert(arg : any, from_type : ArtemisType, to_type : ArtemisType) -> Any:
        '''
        Convert data between Artemis types
        :param arg: Data to convert
        :param from_type: Starting type of data
        :param to_type: Desired type of data
        :return: Converted data
        '''
        if from_type == ArtemisType.LIST and to_type == ArtemisType.NUMPY_ARRAY:
            return np.array(arg)
        if from_type == ArtemisType.NUMPY_ARRAY and to_type == ArtemisType.LIST:
            return arg.tolist()
        return arg

    @staticmethod
    def convert_if(arg : Any, from_type : ArtemisType, to_type : ArtemisType) -> Any:
        '''
        Converts arg from from_type to to_type ONLY if arg is actually of type from_type
        :param arg: Data to convert
        :param from_type: Original type of data
        :param to_type: Desired new type of data
        :return: Converted data
        '''
        if from_type == ArtemisType.LIST and to_type == ArtemisType.NUMPY_ARRAY and isinstance(arg, list):
            return np.array(arg)
        if from_type == ArtemisType.NUMPY_ARRAY and to_type == ArtemisType.LIST and isinstance(arg, np.ndarray):
            return arg.tolist()
        return arg

    @staticmethod
    def assert_true(condition : bool):
        '''
        Assets a condition is true and raises error if not
        :param ondition: Boolean condition
        :return:
        '''
        if not condition:
            raise Exception('[Artemis] ' + inspect.stack()[2][3] + ': Condition is false')

    @staticmethod
    def assert_input_is_type(arg : Any, arg_type) -> None:
        '''
        Asserts that arg is of type type, if not, raise error with helpeful info
        :param arg: Value to check
        :param arg_type: Type we're asserting it must be
        :return: None
        '''
        if not isinstance(arg, arg_type):
            raise Exception(f'[Artemis] Argument given was {arg} and of type {type(arg)} in ' + inspect.stack()[2][3] + ', but arg must be of type ' + str(arg_type))

    @staticmethod
    def escape_path(path : str) -> str:
        '''
        Escapes a path to be compatible with Artemis
        :param path: Path to escape
        :return: Escaped path
        '''

        # Fix local path
        if path.startswith('./'):
            path = os.path.join(os.getcwd(), path[2:])

        return path.replace('\\', '\\\\')

    @staticmethod
    def serialize(data : Any, data_type : ArtemisType, named_args=[]) -> str:
        '''
        Serialize data of type data_type into a str
        :param data: Data to serialize
        :param data_type: Data type of data
        :return: Serialized str data
        '''
        if data_type == ArtemisType.MATPLOTLIB_PLOT:
            data = plt.gcf()
            graph_size = data.get_size_inches() * data.dpi
            graph_data = ArtemisHelper.__b64_encode_bytes(ArtemisHelper.__matplotlib_fig_to_bytes(data))
            graph_size = '100%x*'
            if 'size' in named_args:
                graph_size = named_args['size']

            graph_serialized = {
                'data' : f'![Image]({graph_data} ={graph_size})'
            }
            return ('markdown', graph_serialized)
        if data_type == ArtemisType.MATPLOTLIB_FIGURE:
            graph_size = data.get_size_inches() * data.dpi
            graph_data = ArtemisHelper.__b64_encode_bytes(ArtemisHelper.__matplotlib_fig_to_bytes(data))
            graph_size = '100%x*'
            if 'size' in named_args:
                graph_size = named_args['size']

            graph_serialized = {
                'data' : f'![Image]({graph_data} ={graph_size})'
            }
            return ('markdown', graph_serialized)
        if data_type == ArtemisType.GLB_MODEL:
            try:
                with open(data, 'rb') as file:
                    model_data = ArtemisHelper.__b64_encode_bytes(file.read(), mime_type='data:application/octet-stream')
                    model_serialized = {
                        'data' : model_data
                    }
                    return ('model',model_serialized)
            except Exception as exception:
                print('[Artemis] Error serializing GLB model: ' + str(exception))
                traceback.print_exc()
                return None
        print('[Artemis] Error: ' + inspect.stack()[2][3] + ': data_type must be one of the following: ' + str(ArtemisType))
        return None
    # ================================================================
    # Serialize Functions
    # ================================================================

    @staticmethod
    def __matplotlib_fig_to_bytes(fig) -> bytes:
        '''
        Turns a matplotlib figure into bytes
        :param fig: matplotlib figure
        :return: byte buffer containing matplotlib plot
        '''
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        return buffer.read()

    # ================================================================
    # Serialize Functions
    # ================================================================
    @staticmethod
    def __b64_encode_bytes(data, mime_type='data:image/png') -> str:
        '''
        Encodes bytes using base64 string
        :param data:
        :return: base64 encoded bytes
        '''
        return f"{mime_type};base64," + base64.b64encode(data).decode('utf-8')


    # ================================================================
    # Image Functions
    # ================================================================
    @staticmethod
    def load_image(path : str) -> str: #pylint: disable=unused-private-member
        '''
        Retuns the path if its a web link
        Otherwise, load an image from file and then encodes it in base64
        :param path: Path to image
        :return: Base64 encoded image
        '''

        # Return the URL if we got a URL
        if path.startswith('http') or path.startswith('www'):
            return path

        # Load file as b64
        try:
            with open(path, "rb") as image_file:
                b64_encoding = "data:image/png;base64," + base64.b64encode(image_file.read()).decode('utf-8')
                return b64_encoding
        except Exception as exception:
            print('[Artemis] Exception: Unable to load image')
            print('[Artemis] ' + str(exception))
            traceback.print_stack(limit=3)
        return ""

    @staticmethod
    def __load_gif(path : str) -> str: #pylint: disable=unused-private-member
        '''
        Loads a gif from file and then encodes it in base64
        :param path: Path to GIF
        :return: Base64 encoded GIF
        '''
        try:
            with open(path, "rb") as image_file:
                b64_encoding = "data:image/png;base64," + base64.b64encode(image_file.read()).decode('utf-8')
                return b64_encoding
        except Exception as exception:
            print('[Artemis] Exception: Unable to load image')
            print('[Artemis] ' + str(exception))
        return "'"
