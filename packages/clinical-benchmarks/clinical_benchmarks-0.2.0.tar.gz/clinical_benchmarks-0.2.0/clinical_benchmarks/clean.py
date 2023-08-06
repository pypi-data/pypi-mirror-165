"""Utilities for cleaning data."""
import os

import numpy as np
import pandas as pd
from functools import partial

def clean_fio2(df):
    # unphysiological data
    idx = df['FiO2'] <= 0.2
    df.loc[idx, 'FiO2'] = np.nan

    # proportion instead of percentage
    idx = df['FiO2'] <= 1.0
    df.loc[idx, 'FiO2'] = df.loc[idx, 'FiO2'] * 100.0

    # o2 flow inserted into FiO2
    idx = (df['FiO2'] > 1) & (df['FiO2'] <= 20)
    df.loc[idx, 'FiO2'] = np.nan

    # unphysiological data
    idx = df['FiO2'] >= 100.0
    df.loc[idx, 'FiO2'] = np.nan

    return df


def reject_outlier(low, high, value):
    """Reject anything outside the given boundaries."""
    if value < low:
        return None
    elif value > high:
        return None
    else:
        return value

def clean_instructions():
    """Hard-coded mapping of data type to cleaning function."""
    return {
        'Albumin': partial(reject_outlier, low=1, high=10),
        'Base Excess': partial(reject_outlier, low=0, high=30),
        'Bilirubin Serum': partial(reject_outlier, low=1, high=30),
        "Calcium, Serum": partial(reject_outlier, low=1, high=20),
        "Glucose, Serum Quant": partial(reject_outlier, low=0, high=1000),
        'PaO2': partial(reject_outlier, low=1, high=400),
        "PO2": partial(reject_outlier, low=1, high=400),
        'SaO2': partial(reject_outlier, low=5, high=100),
        "SaO2 %, Arterial": partial(reject_outlier, low=5, high=100),
        "SO2": partial(reject_outlier, low=5, high=100),
        'SPO2': partial(reject_outlier, low=5, high=100),
        'Pulse Oximetry': partial(reject_outlier, low=5, high=100),
        'Resp Rt Tot': partial(reject_outlier, low=5, high=70),
        'Resp Rt': partial(reject_outlier, low=5, high=70),
        'DBP': partial(reject_outlier, low=5, high=300),
        'MAP': partial(reject_outlier, low=5, high=200),
        'SBP': partial(reject_outlier, low=5, high=300),
        # heart rate
        'HR': partial(reject_outlier, low=1, high=300),
        'HR Monitored': partial(reject_outlier, low=1, high=300),
        'Pulse': partial(reject_outlier, low=1, high=300),
        'Pulse Peripheral': partial(reject_outlier, low=1, high=300),
        'HR Apical': partial(reject_outlier, low=1, high=300),
        'Temp': partial(reject_outlier, low=5, high=40),
        'Temp Axillary': partial(reject_outlier, low=5, high=40),
        'Temp Oral': partial(reject_outlier, low=5, high=40),
        'Temp Tympanic': partial(reject_outlier, low=5, high=40),
        'Temp Temporal Artery': partial(reject_outlier, low=5, high=40),
        'Height': partial(reject_outlier, low=0, high=220),
        'Weight': partial(reject_outlier, low=0, high=350),
        'Pain Score': partial(reject_outlier, low=0, high=10),
        "FLACC Pain Scale": partial(reject_outlier, low=0, high=10),
        # hematology cell %s
        'Lymph %': partial(reject_outlier, low=0, high=100),
        'Mono %': partial(reject_outlier, low=0, high=100),
        'Baso %': partial(reject_outlier, low=0, high=100),
        'Neutrophil %': partial(reject_outlier, low=0, high=100),
        'Diff, Eosinophil %': partial(reject_outlier, low=0, high=100),
        'Diff, Granulocyte %': partial(reject_outlier, low=0, high=100),
        'Diff Bands': partial(reject_outlier, low=0, high=100),
        'Imm Granulocytes Cnt Bld Auto, %': partial(reject_outlier, low=0, high=100),
        # hematology cell counts
        'Lymph Abs Cnt': partial(reject_outlier, low=0, high=1000)
    }

def clean_features(df):
    n = 0

    clean_fcns = clean_instructions()
    for col, fcn in clean_fcns.items():
        # skip if not present in df
        if col not in df.columns:
            continue
        
        # apply function that returns None if value is invalid
        df[r] = df[r].apply(fcn)

    # custom outlier rules that use more than just the data value itself

    # weights: (1) remove values with a min 50kg lower than the max
    wt_ids = set(df.loc[df['Weight'] > 270].index)
    wt_min_max = df.loc[wt_ids, 'Weight'].reset_index().groupby(
        df.index.name)['Weight'].agg(['min', 'max', 'count'])
    wt_ids = wt_min_max.loc[(wt_min_max['min'] + 50) < wt_min_max['max']]
    for adm_id in wt_ids.index:
        wt_rem = wt_ids.loc[adm_id, 'min'] + 50
        df.loc[adm_id, 'Weight'] = df.loc[adm_id, 'Weight'].apply(
            lambda x: x if x <= wt_rem else np.nan)

    # remaining patients have their weight converted to kg
    wt_ids = set(df.loc[df['Weight'] > 270].index)
    df.loc[wt_ids, 'Weight'] = df.loc[wt_ids,
                                      'Weight'].apply(lambda x: 0.453592*x)

    return df
