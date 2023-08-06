# Functions to pull in tables, filter timing and join to cohort
from datetime import date
from xmlrpc.client import DateTime
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def join_cohort_data(df_cohort, csv_dir, filter_start_time, filter_stop_time):
    df_cohort_index = df_cohort[['subject_id', 'hadm_id', 'stay_id', 'intime']]

    # use same variables for now for all outcomes, can select custom later
    dynamic_variable_list = [
        'bg', 'blood_differential', 'coagulation', 'chemistry',
        'complete_blood_count', 'enzyme', 'gcs', 'vitalsign', 'weight_durations'
    ]
    static_variable_list = ['age', 'charlson', 'height']
    df_cohort_all_data = df_cohort_index
    for var in static_variable_list:
        logger.info('Joining table: ' + var)
        df_var = read_variable(df_cohort_index, var, csv_dir)
        join_columns = ['subject_id', 'hadm_id', 'stay_id', 'intime']
        df_cohort_all_data = pd.merge(
            df_cohort_all_data,
            df_var,
            how='left',
            on=join_columns,
            suffixes=('', '_' + var)
        )

    # Loops through and combines all the dynamic data, filtering out time windows and averaging
    for var in dynamic_variable_list:
        logger.info('Joining table: ' + var)
        df_var = read_variable(df_cohort_index, var, csv_dir)
        df_var_filtered = filter_variable(
            df_var, var, filter_start_time, filter_stop_time
        )

        num_col = df_var_filtered.select_dtypes(['int64', 'float64','datetime64[ns]'])\
                                                .drop(join_columns, axis=1).columns
        # str_col = df_var_filtered.select_dtypes(['object']).columns

        agg_dict = {}
        num_lambda = ['min', 'max']
        # str_lambda = lambda x: ','.join(x.unique())    # string agg if we wanted to do it
        # for col in str_col:
        #     agg_dict.update({col:str_lambda})

        for col in num_col:
            agg_dict.update({col: num_lambda})
        join_columns = ['subject_id', 'hadm_id', 'stay_id', 'intime']
        df_var_agg = df_var_filtered.groupby(join_columns,
                                             as_index=False).agg(agg_dict)
        df_var_agg.columns = df_var_agg.columns.map(
            lambda x: x[0] if x[0] in join_columns else '_'.join(x)
        )  # join multiindex into single index
        df_cohort_all_data = pd.merge(
            df_cohort_all_data,
            df_var_agg,
            how='left',
            on=join_columns,
            suffixes=('', '_' + var)
        )

    return df_cohort_all_data


def update_column_name(column_name, suffix):
    if column_name in ['subject_id', 'hadm_id', 'stay_id', 'intime']:
        new_column_name = column_name
    else:
        new_column_name = column_name + suffix
    return new_column_name


def filter_variable(df, variable_name, filter_start_time, filter_stop_time):
    date_columns = get_date_columns(variable_name)
    # Add duration column if there is a start_time and end_time
    if date_columns[0] == 'starttime':
        df['duration_' +
           variable_name] = df[date_columns[1]] - df[date_columns[0]]

    # Check if var is a lab, give extra window 6 hours before and 1 day after
    if variable_name in [
        'complete_blood_count', 'chemistry', 'blood_differential',
        'coagulation', 'enzyme'
    ]:
        filter_start_time = filter_start_time - 1 / 4  # 6 hours earlier
        filter_stop_time = filter_stop_time + 1  # 1 day later

    # Check if timestamp within filter bounds
    df["time_diff"] = df[date_columns[0]] - df.intime
    df_filtered = df[(df.time_diff.dt.days >= filter_start_time) &
                     (df.time_diff.dt.days <= filter_stop_time)]

    # drop time_diff and date_column since no longer needed
    if date_columns[
        0] == 'admittime':  # keep this, only age uses this date_column

        df_filtered = df_filtered.drop(['time_diff'], axis=1)
    else:
        df_filtered = df_filtered.drop(['time_diff'] + date_columns, axis=1)
    return df_filtered


def get_date_columns(variable_name):
    if variable_name == 'age':
        date_columns = ['admittime']
    elif variable_name == 'charlson':
        date_columns = []
    elif variable_name == 'suspicion_of_infection':
        date_columns = [
            'antibiotic_time', 'susected_infection_time', 'culture_time'
        ]
    elif variable_name in ['antibiotic', 'heparin']:
        date_columns = ['starttime', 'stoptime']
    elif variable_name in (
        [
            'dobutamine', 'epinephrine', 'norepinephrine', 'phenylephrine',
            'vasopressin', 'ventilation', 'weight_durations'
        ]
    ):

        date_columns = ['starttime', 'endtime']
    else:
        date_columns = ['charttime']
    return date_columns


def get_join_column(variable_name):
    if variable_name == 'age':
        join_columns = ['hadm_id', 'subject_id']
    elif variable_name in ['antibiotic', 'suspicion_of_infection']:
        join_columns = join_columns = ['stay_id', 'hadm_id', 'subject_id']
    elif variable_name in ['heparin', 'rhythm']:
        join_columns = ['subject_id']
    elif variable_name in [
        'crrt', 'dobutamine', 'epinephrine', 'norepinephrine', 'phenylephrine',
        'rrt', 'urine_output', 'vasopressin', 'ventilation', 'weight_durations',
        'suspicion_of_infection'
    ]:
        join_columns = ['stay_id']
    elif variable_name in [
        'gcs', 'height', 'icp', 'oxygen_delivery', 'ventilator_setting',
        'vitalsign'
    ]:
        join_columns = ['stay_id', 'subject_id']
    else:
        join_columns = ['hadm_id', 'subject_id']
    return join_columns


def read_variable(df_cohort, variable_name, csv_dir):
    date_columns = get_date_columns(variable_name)
    join_columns = get_join_column(variable_name)

    df_var = pd.read_csv(
        csv_dir / f"variables/{variable_name}.csv.gz", parse_dates=date_columns
    )

    df_var_with_time = pd.merge(df_cohort, df_var, how='left', on=join_columns)
    return df_var_with_time


def get_lab_features_by_stayid(source_df, stay_id, datetime, columns=None, window=24, agg='last'):
    if type(datetime) != 'datetime64[ns]':
        datetime = pd.to_datetime(datetime) # convert datetime format
    
    window_init_time = datetime - pd.Timedelta(hours=window) # obtain a window

    idx = source_df['stay_id'] == stay_id
    features = source_df.loc[idx]

    # get the features between the time window
    #idx = features['charttime'] >= window_init_time and source_df['charttime'] <= datetime
    idx = features['charttime'].between(window_init_time, datetime)
    features = features.loc[idx]

    if agg is not None:
        features = features.groupby('label').agg(agg)

    if columns is not None:
        features = features.loc[:, columns]
    
    return features