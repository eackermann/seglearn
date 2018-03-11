'''
This module has utilities for time series data input checking
'''
# Author: David Burns
# License: BSD

import numpy as np

def make_ts_data(time_series, context_vars = None):
    '''
    Combines time series data and relational contextual variables into a structure compatible with ``SegPipe`` and related classes.

    Parameters
    ----------
    time_series : array-like, shape [n_series, ]
        Time series data - each element (series) may have a different length
    context_vars : array-like, shape [n_series, n_context_variables]
        contextual relational data

    Returns
    -------
    X : array-like [n_series, ]
        Object containing time series as first column and contextual data if any in second column
    '''
    if context_vars is not None:
        return np.array([[time_series[i], context_vars[i]] for i in range(len(time_series))])
    else:
        return np.array(time_series)

def get_ts_data_parts(X):
    '''
    Separates time series data object into time series variables and contextual variables

    Parameters
    ----------
    X : array-like, shape [n_series, ...]
       Time series data and (optionally) contextual data created as per ``make_ts_data``

    Returns
    -------
    Xt : array-like, shape [n_series, ]
        Time series data from first column of X
    Xs : array-like, shape [n_series, n_contextd = np.colum _variables]
        contextual variables from columns 2

    '''
    if X.dtype == np.object and X.ndim == 2:
        irange = np.arange(len(X))
        Xt = np.array([X[i,0] for i in irange])
        Xs = np.array([X[i,1] for i in irange])
        return Xt, Xs
    else:
        return np.array(X), None


def check_ts_data(X):
    '''
    Checks time series data is good. If not raises assertion error.

    Parameters
    ----------
    X : array-like, shape [n_series, ...]
       Time series data and (optionally) contextual data created as per ``make_ts_data``

    '''
    Xt, Xs = get_ts_data_parts(X)
    if Xs is not None:
        assert len(Xt) == len(Xs)
    N_tvars = np.array([np.row_stack(Xt[i]).shape[1] for i in range(len(Xt))])
    assert len(np.unique(N_tvars)) == 1

def ts_stats(Xt, y, fs = 1.0, class_labels = None):
    '''
    Generates some helpful statistics about the data X

    Parameters
    ----------
    X : array-like, shape [n_series, ...]
       Time series data and (optionally) contextual data created as per ``make_ts_data``
    y : array-like, shape [n_series]
        target data
    fs : float
        sampling frequency
    class_labels : list of strings, default None
        List of target class names


    Returns
    -------
    results : dict
        | Dictionary of relevant statistics for the time series data
        | results['total'] has stats for the whole data set
        | results['by_class'] has stats segragated by target class

    '''
    check_ts_data(Xt)
    Xt, Xs = get_ts_data_parts(Xt)

    if Xs is not None:
        S = len(np.atleast_1d(Xs[0]))
    else:
        S = 0

    C = np.max(y) + 1 # number of classes
    if class_labels is None:
        class_labels = np.arange(C)

    N = len(Xt)
    if Xt[0].ndim > 1:
        D = Xt[0].shape[1]
    else:
        D = 1

    Ti = np.array([Xt[i].shape[0] for i in range(N)], dtype=np.float64) / fs
    ic = np.array([y == i for i in range(C)])
    Tic = [Ti[ic[i]] for i in range(C)]

    T = np.sum(Ti)

    total = {"n_series": N, "n_classes": C, "n_TS_vars": D, "n_context_vars": S, "Total_Time": T,
              "Series_Time_Mean": np.mean(Ti),
              "Series_Time_Std": np.std(Ti),
              "Series_Time_Range": (np.min(Ti), np.max(Ti))}

    by_class = {"Class_labels": class_labels,
                "n_series": np.array([len(Tic[i]) for i in range(C)]),
                "Total_Time": np.array([np.sum(Tic[i]) for i in range(C)]),
                "Series_Time_Mean": np.array([np.mean(Tic[i]) for i in range(C)]),
                "Series_Time_Std": np.array([np.std(Tic[i]) for i in range(C)]),
                "Series_Time_Min": np.array([np.min(Tic[i]) for i in range(C)]),
                "Series_Time_Max": np.array([np.max(Tic[i]) for i in range(C)])}

    results = {'total': total,
               'by_class': by_class}

    return results















