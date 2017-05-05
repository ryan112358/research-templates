import argparse
import pandas as pd
import numpy as np
from IPython import embed
import itertools
from random import shuffle
import time

"""
This is a simple description of functionality of this program.
"""

def run_parallel(names, params):
    """
    Run experiments in parallel using MPI

    :param names: a list of names of the parameters
    :param params: a list of parameter settings to run experiments for
    :returns: a pandas dataframe with results

    Note: To setup your environment on ubuntu:
        $ sudo apt-get install libmpich-dev
        $ pip install mpi4py
        $ mpirun -n 4 python experiments.py
    """
    from mpi4py import MPI
    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()
    size = comm.Get_size()
    if rank == 0:
        work = list(params)
        shuffle(work)
        for i in range(1, size):
            comm.send(work[i::size], dest=i, tag=1)
        tasks = work[0::size]
    else:
        tasks = comm.recv(source=0, tag=1)

    local = run_experiments(names, tasks)
    results = comm.gather(local, root=0)   
    if rank == 0:
        index = pd.MultiIndex.from_tuples(params, names=names)
        return pd.concat(results).reindex(index)

def run_experiments(names, params):
    """
    Run experiments and return results as a pandas data frame

    :param names: a list of names of the parameters
    :param params: a list of parameter settings to run experiments for
    :returns: a pandas dataframe with results

    """
    index = pd.MultiIndex.from_tuples(params, names=names)
    results = pd.DataFrame(index=index, columns=['error', 'time'], dtype=float)
    for setting in params:
        t0 = time.time()
        result = run_experiment(setting)
        t1 = time.time()
        results.loc[setting] = np.random.rand(2)
    return results

# should this be made a class?
def run_experiment(setting):
    N, trial = setting
    pass

def get_all_settings(*params):
    """
    Create the experiment tuples to run from the range of experiment settings
    over each individual parameter
    :param param1: parameter settings for first parameter (can be a list or a single item)
    :param param2: parameter settings for second parameter (can be a list or a single item)
    :param ...: ...
    :return: a list of parameter setting tuples

    >>> get_all_settings([1,2,3], True, ['x', 'y'])
    [(1, True, 'x'),
     (1, True, 'y'),
     (2, True, 'x'),
     (2, True, 'y'),
     (3, True, 'x'),
     (3, True, 'y')] 
    """
    params2 = [p if type(p) is list else [p] for p in params]
    return list(itertools.product(*params2))

def test(parallel = False):
    params = itertools.product([10,50,100], [1,2,3,4,5])
    if not parallel:
        result = run_experiments(['N', 'trial'], list(params))
    else:
        result = run_parallel(['N', 'trial'], list(params))
    return result    

def default_params():
    """
    Return default parameters to run this program

    :returns: a dictionary of default parameter settings for each command line argument
    """
    params = {}
    params['parallel'] = False

    return params

if __name__ == '__main__':
    description = ''
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=description, formatter_class=formatter)
    parser.add_argument('--parallel', action='store_true', help='use mpi to parallelize experiments')

    parser.set_defaults(**default_params()) 
    args = parser.parse_args()

    result = test(args.parallel)
    print result
