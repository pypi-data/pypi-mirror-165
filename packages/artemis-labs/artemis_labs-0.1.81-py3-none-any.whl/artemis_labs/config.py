'''
This custom config file is where you can create functions for custom component types for your
@output decorators
'''

# pylint: disable=line-too-long
# pylint: disable=too-many-branches
# pylint: disable=pointless-string-statement
# pylint: disable=unused-argument
# pylint: disable=self-assigning-variable
# pylint: disable=invalid-name
# pylint: disable=unused-import

import sys
import datetime
import io
import inspect
import base64
import typing
from typing import List, Dict, Any, Tuple

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from .artemis_helper import ArtemisHelper, ArtemisType
from .artemis_config_manager import ArtemisConfigManager

# ========================================================
# WARNING: DO NOT EDIT
def setup_plot_args(named_args_dict : Dict) -> None:
    '''
    Uses dictionary of named_args_dict to customize matplotlib graph
    :param named_args_dict: Dictionary of named args
    :return: None
    '''

    # Graph parameters
    xmin = None
    xmax = None
    ymin = None
    ymax = None
    figsize = (8,3)
    xlabel = ""
    ylabel = ""
    title = ""

    # Run args
    if 'xmin' in named_args_dict:
        xmin = float(named_args_dict['xmin'])
    if 'xmax' in named_args_dict:
        xmax = float(named_args_dict['xmax'])
    if 'ymin' in named_args_dict:
        ymin = float(named_args_dict['ymin'])
    if 'ymax' in named_args_dict:
        ymax = float(named_args_dict['ymax'])
    if 'xlabel' in named_args_dict:
        xlabel = named_args_dict['xlabel']
    if 'ylabel' in named_args_dict:
        ylabel = named_args_dict['ylabel']
    if 'title' in named_args_dict:
        title = named_args_dict['title']
    if 'figsize' in named_args_dict:
        figsize_input = named_args_dict['figsize'].replace(')', '').replace('(', '')
        figsize_components = figsize_input.split(',')
        figsize = (float(figsize_components[0]), float(figsize_components[1]))

    # Make plot
    plt.figure(figsize=figsize)

    # Set limits
    if xmin is not None:
        plt.xlim(left=xmin)
    if xmax is not None:
        plt.xlim(right=xmax)
    if ymax is not None:
        plt.ylim(top = ymax)
    if ymin is not None:
        plt.ylim(bottom=ymin)

    # Set labels
    if xlabel != '':
        plt.xlabel(xlabel)
    if ylabel != '':
        plt.ylabel(ylabel)

    # Set title
    if title != '':
        plt.title(title)
# ========================================================

# ========================================================
# Run Information and Fields
# ========================================================
def get_run_information() -> Dict:
    '''
    User-defined function which returns the information which
    appears in the first card when you launch Artemis
    :return: Dictionary of run information for the first card in any Artemis notebook
    '''
    run_information = {
        'Run Date' : __file__.replace("\\", "/").replace(" ", "%20"),
        'System Type' : sys.platform,
        'System Version' : sys.version,
        'Date' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return run_information

def get_fields() -> Dict:
    '''
    User defined function which returns custom fields
    which can be referenced throughout the code by writing
    %%field_name$$
    '''
    fields = {
        'author' : 'Austin McCoy',
        'email' : 'austinmccoy@artemisar.com',
        'white' : 'rgb(255,255,255)',
        'logo' : 'https://www.artemisdevtool.com/Assets/images/logo_trim.png',
        'variable' : 'x'
    }
    return fields

# ========================================================
# Custom Anchors
# ========================================================

'''
Available output types:
- graph
- heading

Required return type: Tuple

Required function format (arg, named_args_dict)
'''

def graph(fig, named_args_dict : Dict) -> Tuple:
    '''
    This takes in a matplotlib figure and named args,
    and returns a serialized form of the matplotlib figure
    :param fig: Matplotlib figure
    :param named_args: Named arguments provided when invoking decorator
    :return: Serialized matplotlib figure
    '''

    # Validate input
    ArtemisHelper.assert_input_is_type(fig, plt.Figure)

    # Return serialized data
    return ArtemisHelper.serialize(fig, ArtemisType.MATPLOTLIB_FIGURE, named_args_dict)

ArtemisConfigManager.register_function(graph, 'graph')

def line_graph(arr, named_args_dict : Dict) -> Tuple:
    '''
    This plots a line graph from either arr (a 2D container of numerical values passed in through the data named arg) OR
    data-x and data-y named args (if no data named arg is supplied):
    Example Use 1: # @output line_graph data=[[1,2,3],[4,5,6]]
    Example Use 2: # @output line_graph data-x=[1,2,3] data-y=[4,5,6]
    :param arr: Container of values to graph (List or Numpy) ONLY if data named arg is supplied, ELSE NONE
    :param named_args_dict: Named arguments provided when invoking decorator
    :return: Serialized line graph
    '''

    # Check if we are using data-x data-y mode
    if 'data-x' in named_args_dict and 'data-y' in named_args_dict:

        # Get arrays
        arr_x = named_args_dict['data-x']
        arr_y = named_args_dict['data-y']

        # Convert
        arr_x = ArtemisHelper.convert_if(arr_x, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)
        arr_y = ArtemisHelper.convert_if(arr_y, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)

        # Check dimensionaliy
        ArtemisHelper.assert_true(arr_x.ndim == 1)
        ArtemisHelper.assert_true(arr_y.ndim == 1)

        # Setup plot arguments
        setup_plot_args(named_args_dict)

        # Actually plot data
        plt.plot(arr_x, arr_y)

    else:

        # Regular plotting mode

        # Convert type to numpy array if it is a list
        arr = ArtemisHelper.convert_if(arr, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)

        # Validate input
        ArtemisHelper.assert_input_is_type(arr, np.ndarray)

        # Reshape data for line plot
        if arr.ndim == 2:
            if arr.shape[1] == 2:
                arr = arr
            elif arr.shape[0] == 2:
                arr = np.array(list(zip(arr[0], arr[1])))
            else:
                return None

        # Setup plot arguments
        setup_plot_args(named_args_dict)

        # Actually plot data
        if arr.ndim == 1:
            plt.plot(arr)
        elif arr.ndim == 2:
            plt.plot(arr[:,0], arr[:,1])

    # Serialize plot
    serialized_plot = ArtemisHelper.serialize(None, ArtemisType.MATPLOTLIB_PLOT, named_args_dict)

    # Close figure
    plt.close()

    # Return serialized plot
    return serialized_plot

ArtemisConfigManager.register_function(line_graph, 'line-graph')

def scatter_graph(arr , named_args_dict : Dict) -> Tuple:
    '''
    This takes in a container of numerical values and named args,
    plots a scatter plot using those numerical values, using
    named arguments to customize the graph,
    and returns a serialized form of the matplotlib figure
    :param arr: Container of values to graph (List or Numpy)
    :param named_args_dict: Named arguments provided when invoking decorator
    :return: Serialized scatter graph
    '''

    # Setup plot arguments
    setup_plot_args(named_args_dict)

    # Check if we are using data-x data-y mode
    if 'data-x' in named_args_dict and 'data-y' in named_args_dict:

        # Get arrays
        arr_x = named_args_dict['data-x']
        arr_y = named_args_dict['data-y']

        # Convert
        arr_x = ArtemisHelper.convert_if(arr_x, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)
        arr_y = ArtemisHelper.convert_if(arr_y, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)

        # Check dimensionaliy
        ArtemisHelper.assert_true(arr_x.ndim == 1)
        ArtemisHelper.assert_true(arr_y.ndim == 1)

        # Actually plot data
        plt.scatter(arr_x, arr_y)
    else:

        # Convert type to numpy array if it is a list
        arr = ArtemisHelper.convert_if(arr, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)

        # Validate input
        ArtemisHelper.assert_input_is_type(arr, np.ndarray)

        # Reshape data for line plot
        if arr.ndim == 2:
            if arr.shape[1] == 2:
                arr = arr
            elif arr.shape[0] == 2:
                arr = np.array(list(zip(arr[0], arr[1])))
            else:
                return None

        # Actually plot data
        if arr.ndim == 2:
            plt.scatter(arr[:,0], arr[:,1])

    # Serialize plot
    serialized_plot = ArtemisHelper.serialize(None, ArtemisType.MATPLOTLIB_PLOT, named_args_dict)

    # Close figure
    plt.close()

    # Return serialized plot
    return serialized_plot

ArtemisConfigManager.register_function(scatter_graph, 'scatter-graph')

def histogram(arr , named_args_dict : Dict) -> Tuple:
    '''
    This takes in a 1D container of numerical values and named args,
    plots a histogram using those numerical values, using
    named arguments to customize the graph,
    and returns a serialized form of the matplotlib figure
    :param arr: 1D container of values to graph (List or Numpy)
    :param named_args_dict: Named arguments provided when invoking decorator
    :return: Serialized histogram
    '''

    # Convert type to numpy array if it is a list
    arr = ArtemisHelper.convert_if(arr, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)

    # Validate input
    ArtemisHelper.assert_input_is_type(arr, np.ndarray)

    # Setup plot arguments
    setup_plot_args(named_args_dict)

    # Actually plot data
    plt.hist(arr, 50)

    # Serialize plot
    serialized_plot = ArtemisHelper.serialize(None, ArtemisType.MATPLOTLIB_PLOT, named_args_dict)

    # Close figure
    plt.close()

    # Return serialized plot
    return serialized_plot

ArtemisConfigManager.register_function(histogram, 'histogram')

def line_graph_x_y_z(arr , named_args_dict : Dict) -> Tuple:
    '''
    This takes in three arrays of numerical values through named arguments
    data-x, data-y, and data-z, and it uses these arrays to create a 3D surface plot.
    It also takes in named arguments title, x-label, y-label, and z-label, and it uses
    these to customize the graph.

    :param arr: None
    :param named_args_dict: Named arguments provided when invoking decorator
    :return: Serialized surface graph
    '''

    # Unpack
    x = named_args_dict['data-x']
    y = named_args_dict['data-y']
    z = named_args_dict['data-z']

    # Convert type to numpy arrays if lists
    x = ArtemisHelper.convert_if(x, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)
    y = ArtemisHelper.convert_if(y, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)
    z = ArtemisHelper.convert_if(z, ArtemisType.LIST, ArtemisType.NUMPY_ARRAY)

    # Plot args
    setup_plot_args(named_args_dict)

    ax = plt.axes(projection='3d')
    ax.plot_trisurf(x, y, z, cmap='viridis', linewidth=0.1)

    # Serialize plot
    serialized_plot = ArtemisHelper.serialize(None, ArtemisType.MATPLOTLIB_PLOT, named_args_dict)

    # Close figure
    plt.close()

    # Return serialized plot
    return serialized_plot
ArtemisConfigManager.register_function(line_graph_x_y_z, 'line_graph_x_y_z')


def model(arr , named_args_dict : Dict) -> Tuple:
    '''
    This takes in the file path to a 3D GLB model, and it returns a serialized
    form of the model.

    :param arr: None
    :param named_args_dict: Named arguments provided when invoking decorator
    :return: Serialized model
    '''

    # Validate type
    ArtemisHelper.assert_input_is_type(arr, str)

    # Escape path
    arr = ArtemisHelper.escape_path(arr)

    print("Loading model from: " + arr)

    # Return serialized model
    return ArtemisHelper.serialize(arr, ArtemisType.GLB_MODEL, named_args_dict)
ArtemisConfigManager.register_function(model, 'model')
