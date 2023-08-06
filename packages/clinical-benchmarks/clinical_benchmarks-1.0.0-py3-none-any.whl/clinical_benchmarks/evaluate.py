"""Measures for evaluating the performance of models."""

from sklearn.metrics import roc_auc_score
from sklearn.metrics import mean_squared_error
from math import sqrt

def model_accuracy(outcome, y_test, y_pred):
    if outcome == 'los_icu':
        model_score = sqrt(mean_squared_error(y_test, y_pred))
    elif outcome == 'mortality':
        model_score = roc_auc_score(y_test, y_pred)
    else:
        model_score = roc_auc_score(y_test, y_pred)

    return model_score