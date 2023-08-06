import pandas as pd
from pathlib import Path
import logging

from clinical_benchmarks.merge import join_cohort_data

logger = logging.getLogger(__name__)

# read the downloaded feature query csv files
def read_feature_table(feature:str, csv_dir:Path) -> pd.DataFrame:
    filename = feature + ".csv.gz"
    filepath = csv_dir / filename

    try:
        feature_df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise Exception(f"file {filename} dose not exist")

    feature_df = feature_df.sort_values(by=['subject_id'])
    if 'charttime' in feature_df.columns:
        feature_df['charttime'] = pd.to_datetime(feature_df['charttime'])
    return feature_df


# read the downloaded cohort query csv files
def read_cohort_data(cohort_name:str, csv_dir:Path):
    filename = cohort_name + '.csv.gz'
    filepath = csv_dir / filename

    try:
        cohort_df = pd.read_csv(filepath, parse_dates=['starttime', 'endtime'])
    except FileNotFoundError:
        raise Exception(f"cohort {cohort_name} dose not exist")
    
    cohort_df = cohort_df.sort_values(by=['subject_id'])
    return cohort_df


# read the downloaded outcome task query csv files and merge to specified cohort
def read_cohort_task(task_name:str, cohort_name:str, csv_dir:Path) -> pd.DataFrame:
    df_cohort = read_cohort_data(cohort_name, csv_dir)

    task_table = {
        "mortality" : ("hospital_expire_flag", "mortality.csv.gz"),
        "los_icu" : ("los_icu", "los_icu.csv.gz"),
        "dialysis" : ("dialysis_active", "los_icu.csv.gz"),
        "inv_vent" : ("inv_vent_flag", "inv_vent.csv.gz"),
        "vancomycin_dose" : ("dose_due", "vancomycin_dose.csv.gz"),
        "vancomycin_level" : ("vancomycin_level", "vancomycin_level.csv.gz"),
        "heparin_dose" : ("dose_due", "heparin_dose.csv.gz")
    }

    try:
        task_label = task_table[task_name][0]
        df_task = pd.read_csv(csv_dir / task_table[task_name][1])
    except KeyError:
        raise Exception(f"task {task_name} dose not exist")

    df_cohort = pd.merge(df_cohort, df_task, how='left', on=['subject_id'])
    if 'charttime' in df_cohort.columns:
        df_cohort['charttime'] = pd.to_datetime(df_cohort['charttime'])
    return task_label, df_cohort


def filter_cohort_task(df_cohort, task_label, args):
    """ Filter cohorts and task tables by los, start_time and stop_time """
    # Create base cohorts
    df_cohort_filtered = df_cohort[(df_cohort.los >= args.filter_los)]
    df_cohort_filtered = df_cohort_filtered.drop(columns=['los'])

    if args.task == 'dialysis':
        df_cohort_filtered = df_cohort_filtered[
            (df_cohort_filtered.dialysis_present == 0) | (
                (df_cohort_filtered.dialysis_present == 1) &
                (df_cohort_filtered.dialysis_start_time > 24)
            )]
        df_cohort_filtered.drop(
            ['dialysis_present', 'dialysis_start_time'], axis=1, inplace=True
        )
    df_task_filtered = df_cohort_filtered[task_label]
    df_cohort_filtered.drop([task_label], axis=1, inplace=True)

    # Filter data into window of time
    df_cohort_data = join_cohort_data(
        df_cohort_filtered, args.csv_dir, args.filter_start_time,
        args.filter_stop_time
    )
    return df_cohort_data, df_task_filtered


def export_cohort_data(df_inputs, df_outputs, args):
    """ Export cohort and task tables to allow for better reprodcucibility """
    str_inputs = args.csv_dir / f"""cohort_all_data_los{args.filter_los:0.1f}_
                    span_{args.filter_start_time:0.1f}-
                    {args.filter_stop_time:0.1f}
                    .csv""".replace('\n', '').replace(' ', '')
    str_outputs = args.csv_dir / f"""task_{args.task}_
                    los{args.filter_los:0.1f}_
                    span_{args.filter_start_time:0.1f}-
                    {args.filter_stop_time:0.1f}
                    .csv""".replace('\n', '').replace(' ', '')

    df_inputs.to_csv(str_inputs)
    df_outputs.to_csv(str_outputs)