import argparse
import pandas as pd
import numpy as np
from IPython import embed

"""
This is a simple description of functionality of this program.
"""


# http://docs.python-guide.org/en/latest/writing/documentation/
def documented(param1, param2):
    """
    This is a reST style.

    :param param1: this is a first param
    :param param2: this is a second param
    :returns: this is a description of what is returned

    >>> documented(0, 0)
    0
    """
    return 0

def default_params():
    """
    Return default parameters to run this program

    :returns: a dictionary of default parameter settings for each command line argument
    """
    params = {}

    return params

if __name__ == '__main__':
    description = ''
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)

    parser.set_defaults(**default_params()) 
    args = parser.parse_args()


