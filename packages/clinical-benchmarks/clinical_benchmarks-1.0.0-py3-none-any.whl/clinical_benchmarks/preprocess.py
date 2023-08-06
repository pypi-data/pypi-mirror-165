"""Utilities for preprocessing extracted datasets."""
import numpy as np
import pandas as pd
from scipy import stats

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    StandardScaler, OneHotEncoder, OrdinalEncoder
)
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.base import TransformerMixin


class DropMissingFeatures(TransformerMixin):
    def __init__(self, thresh):
        self.thresh = thresh
        self.drop_features = []

    def fit(self, X, y):
        self.drop_features = [
            c for c in X if X[c].isnull().sum() / len(X) > self.thresh
        ]
        return self

    def transform(self, X, y=None):
        X_ = X.drop(columns=self.drop_features)
        return X_


class DropSpecificFeatures(TransformerMixin):
    def __init__(self, drop_features):
        self.drop_features = drop_features

    def fit(self, X, y):
        # check that features are actually in X
        self.drop_features = [c for c in self.drop_features if c in X]
        return self

    def transform(self, X, y=None):
        X_ = X.drop(columns=self.drop_features)
        return X_


def custom_preprocessor(df_inputs, df_outputs, model_type):
    categorical_features = df_inputs.select_dtypes(include=['object']).columns
    numeric_features = df_inputs.select_dtypes(
        include=['int64', 'float64']
    ).columns

    transformers = []
    numeric_transformer = Pipeline(
        steps=[
            ('drop_missing', DropMissingFeatures(0.98)),
            ('drop_specific', DropSpecificFeatures(['fio2_min', 'fio2_max'])),
            ('imputer', SimpleImputer(missing_values=np.nan, strategy='mean')
            ), ('scaler', StandardScaler())
        ]
    )
    transformers.append(('num', numeric_transformer, numeric_features))

    if model_type == 'xgb':
        encoder = OrdinalEncoder()
    else:
        encoder = OneHotEncoder(handle_unknown='ignore')
    categorical_transformer = Pipeline(
        steps=[
            ('drop_missing', DropMissingFeatures(0.98)),
            (
                'imputer',
                SimpleImputer(strategy='constant', fill_value='MISSING')
            ), ('encoder', encoder)
        ]
    )
    transformers.append(('cat', categorical_transformer, categorical_features))

    return ColumnTransformer(transformers=transformers)


def drop_feature_na_percent(df, na_percent=0.98, drop_features=[]):
    """ Remove features with greater than na_percent missing data """
    drop_columns = [
        c for c in df if df[c].isnull().sum() / len(df) > na_percent
    ]
    drop_columns.extend(drop_features)
    df = df.drop(columns=drop_columns)
    return df


def impute_using_additive_formula(df, a, b, c, verbose=True):
    """
    If we know a = b + c, we can impute data
    Many features are related in this way
    e.g. Total protein, albumin, globulin
    
    This is useful for merging features and reducing redundancy in the
    feature space.
    """

    if verbose:
        print(f'{a} = {b} + {c}')
    # === impute a ===
    # first we need b and c to not be null
    idx = df[b].notnull() & df[c].notnull()
    # rows where a is null
    idx = idx & df[a].isnull()
    # a = b + c
    df.loc[idx, a] = df.loc[idx, b] + df.loc[idx, c]
    if verbose:
        n = idx.sum()
        print(f'{a} - Imputed {n} values')

    # === impute b ===
    idx = df[a].notnull() & df[c].notnull()
    # rows where b is null
    idx = idx & df[b].isnull()
    # b = a - c
    df.loc[idx, b] = df.loc[idx, a] - df.loc[idx, c]
    if verbose:
        n = idx.sum()
        print(f'{b} - Imputed {n} values')

    # === impute c ===
    idx = df[a].notnull() & df[b].notnull()
    # rows where c is null
    idx = idx & df[c].isnull()
    # c = a - b
    df.loc[idx, c] = df.loc[idx, a] - df.loc[idx, b]
    if verbose:
        n = idx.sum()
        print(f'{c} - Imputed {n} values')

    return df


def _q25(x):
    """
    Compute percentile (25th)
    """
    return np.nanpercentile(x.values, 25)


def _q75(x):
    """
    Compute percentile (75th)
    """
    return np.nanpercentile(x.values, 75)


def _std(x, ddof=1):
    """
    Compute standard deviation with ddof degrees of freedom
    """
    return np.nanstd(x.values, ddof=ddof)


def _range(x):
    """
    Compute range (max-min)
    """
    return max(x) - min(x)


def _first(x):
    """
    Get first
    """
    return x.iloc[0]


def _last(x):
    """
    Get last
    """
    return x.iloc[-1]


def _slope(df, timecol):
    """
    get the slope
    """
    d = {}
    for col in df.columns:
        if col == timecol:
            continue
        ts = df[[timecol, col]].dropna()
        x = ts[timecol]
        y = ts[col]
        try:
            slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
        except ValueError:
            slope = np.nan
        d[f'_slope_{col}'] = slope

    return pd.Series(d)
