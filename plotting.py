import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython import embed


"""
This is a simple description of functionality of this program.
"""


# http://docs.python-guide.org/en/latest/writing/documentation/
def plot_figure(param1, param2):
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
    params['load'] = None
    params['style'] = 'ggplot'
    params['show'] = True
    params['save'] = None
    return params

if __name__ == '__main__':
    description = 'plotting stuff'
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)
    parser.add_argument('--load', type=str, help='data to load for plotting')
    parser.add_argument('--style', choices=plt.style.available, help='style of plot')
    parser.add_argument('--show', action='store_true', help='show the plot')
    parser.add_argument('--save', type=str, help='path to output image') 

    parser.set_defaults(**default_params()) 
    args = parser.parse_args()
    assert args.load, 'must provide data to plot'
    if args.style:
        plt.style.user(args.style)
    data = pd.read_csv(args.load, index_col=None)
    
    if args.save:
        plt.savefig(args.save)
    if args.show:
        plt.show()
