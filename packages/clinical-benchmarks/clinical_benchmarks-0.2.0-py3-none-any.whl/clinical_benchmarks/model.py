"""Classes and utilities for training machine learning models."""
import logging
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import (LogisticRegression, LinearRegression)
import xgboost as xgb

from clinical_benchmarks.evaluate import model_accuracy
from clinical_benchmarks.preprocess import custom_preprocessor
from clinical_benchmarks.utils import read_cohort_task
from clinical_benchmarks.utils import filter_cohort_task
from clinical_benchmarks.utils import export_cohort_data

logger = logging.getLogger(__name__)


def train_task(X_train, y_train, preprocessor, task, model_type):
    if (model_type == 'lr') & (task == 'los_icu'):
        mdl = LinearRegression()
    elif model_type == 'lr':
        mdl = LogisticRegression(max_iter=1000)
    elif model_type == 'xgb':
        mdl = xgb.XGBRegressor()
        params = {
            'learning_rate': 0.1,
            'gamma': 0.5,
            'max_depth': 10,
            'colsample_bytree': 0.8,
            'subsample': 0.9,
            'min_child_weight': 5,
            'n_estimators': 250,
            'eval_metric': 'logloss',
            'use_label_encoder': False
        }
        mdl.set_params(**params)
    else:
        logger.error(f"Model type '{model_type}' is invalid")

    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', mdl)])
    model = pipeline.fit(X_train, y_train.values.ravel())
    return pipeline, model


def predict_task(args):
    task_label, df_cohort = read_cohort_task(args.task, args.cohort_name, args.csv_dir)
    df_inputs, df_outputs = filter_cohort_task(df_cohort, task_label, args)

    preprocessor = custom_preprocessor(df_inputs, df_outputs, args.model_type)
    X_train, X_test, y_train, y_test = train_test_split(
        df_inputs, df_outputs, test_size=0.25, random_state=42
    )
    pipeline, model = train_task(
        X_train, y_train, preprocessor, args.task, args.model_type
    )
    y_pred = pipeline.predict(X_test)

    model_acc = model_accuracy(args.task, y_test, y_pred)
    logger.info(f'{args.task} accuracy: {model_acc:0.3f}')
    # write out cohort data used
    export_cohort_data(df_inputs, df_outputs, args)
    return model, y_pred, y_test
