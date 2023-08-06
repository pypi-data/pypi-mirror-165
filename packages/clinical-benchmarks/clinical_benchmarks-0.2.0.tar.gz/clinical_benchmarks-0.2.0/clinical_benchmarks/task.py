import pandas as pd
import os
import numpy as np
from pathlib import Path
from utils import read_cohort_task, read_feature_table, read_cohort_data

# rename to preprocessor
# drop the task name, output the final dataframe to a file
class BaseDataProcessor(object):
    def __init__(self):
        # load environment variables and necessary query tables
        self.csv_dir = Path(os.environ['MODEL_DIR']) # read dir path from environment variable
        self.chemistry_feature = read_feature_table('chemistry', self.csv_dir)
        self.coagulation_feature = read_feature_table('coagulation', self.csv_dir)
        self.blood_feature = read_feature_table('complete_blood_count', self.csv_dir)
        self.vitalsign_feature = read_feature_table('vitalsign', self.csv_dir)
        self.weight_feature = read_feature_table('weight', self.csv_dir)
        self.height_feature = read_feature_table('height', self.csv_dir)

    '''
        @param: {start, stop} two integer represent how long a time window is
        @param: {agg} a method of aggregation, ie. last
        @param: {feature} feature that need extract and aggregate
        @param: {columns} specific columns that want return
        @return aggregated features in a specified time offset between start and stop
                the time offset is counted from the ICU intime
    '''
    def get_feature_data(self, start:int, stop:int, agg:str, feature:pd.DataFrame, columns=None) -> pd.DataFrame:
        start = pd.Timedelta(start, 'h')
        stop = pd.Timedelta(stop, 'h') # convert to hour for computing time offset

        # convert chartime to event time, depend on event type
        feature['charttime'] = pd.to_datetime(feature['charttime'])
        intime_col = self.task_df[['subject_id', 'intime', 'outtime']]
        intime_col = intime_col.drop_duplicates()

        feature_df = feature.merge(intime_col, how='inner', on=['subject_id']) # add in the intime col to compute offset

        # filter out the lab result dose belong to current ICU admission/duration
        feature_df['valid'] = feature_df.apply(lambda x: 1 if (x['charttime'] > x['intime'] and x['charttime'] < x['outtime']) else 0, axis=1)
        idx = feature_df['valid'] != 1
        feature_df = feature_df.drop(feature_df.loc[idx].index, axis=0) # drop the records outside ICU admission
        feature_df = feature_df.drop('valid', axis=1)

        # compute time offset column for each feature since ICU admission time / intime
        feature_df['event_time_offset'] = feature_df['charttime'] - feature_df['intime']
        feature_df = feature_df.drop(['intime', 'outtime'], axis=1)

        # locate the feature event that happens during desired period
        idx = feature_df['event_time_offset'].between(start, stop)
        feature_df = feature_df.loc[idx].sort_values(by='charttime')

        # aggregate the features for each subject
        feature_df = feature_df.groupby(['subject_id']).agg(agg)

        if columns is not None:
            feature_df = feature_df.loc[:, columns]
        
        return feature_df


    '''
        @param: {cohort_df} a subject cohort from a task object
        @param: {timestep} a str value stated in hour, represent the increment of time from ICU starttime to endtime
        @return: a time series dataframe with timestep increment for each subject
    '''
    def create_time_cohort(self, cohort_df:pd.DataFrame, time_step:int) -> pd.DataFrame:
        time_step = str(time_step) + 'H'
        cohort_with_time = pd.DataFrame({})
        cohort_df['starttime'] = pd.to_datetime(cohort_df['starttime'])
        cohort_df['endtime'] = pd.to_datetime(cohort_df['endtime'])
        for _, row in cohort_df.iterrows():
            to_insert = pd.date_range(row['starttime'], row['endtime'], freq=time_step)
            to_insert = pd.DataFrame(to_insert)
            to_insert['subject_id'] = row['subject_id']
            to_insert['episode_id'] = row['episode_id']
            cohort_with_time = pd.concat([cohort_with_time, to_insert])

        cohort_with_time = cohort_with_time.rename(columns={0 : 'time'})
        return cohort_with_time


    '''
        merge feature table into a time series cohort
        @param: {cohort_with_time} the outcome dataframe return by method {create_time_cohort}
        @param: {feature} the feature dataframe that want to merge in
        @param: {cohort_df} the cohort dataframe of the current Task object, ie. VancomycinDosing.cohort_df
        @prarm: {time_step} a integer that represent how many hours will last for a time window
        @return return a cohort_with_time dataframe that each time step matches with a feature measurement, might have None for a time step
    '''
    def merge_feature_to_time_dataframe(self, cohort_with_time:pd.DataFrame, feature:pd.DataFrame, cohort_df:pd.DataFrame, agg:str, time_step:int):
        feature_df = cohort_df.merge(feature, how='inner', on='subject_id')
        # first filter the feature events that happens outside the ICU stay time
        feature_df = feature_df.loc[(feature_df['charttime'] >= feature_df['starttime']) & (feature_df['charttime'] <= feature_df['endtime'])]
        feature_df = feature_df.sort_values(by='charttime').reset_index()
        feature_df = feature_df.drop(['starttime', 'endtime', 'index'], axis=1)

        res = cohort_with_time.merge(feature_df, how='inner', on=['subject_id', 'episode_id'])
        # match each feature measurement to the corresponding time window defined by the time_step
        # ie. between 4:00 to 4:00 + time_step
        res = res.loc[(res['charttime'] >= res['time']) & (res['charttime'] <= res['time'] + pd.Timedelta(time_step, 'h'))]
        res = res.groupby(by=['episode_id', 'time']).agg(agg)
        res = cohort_with_time.merge(res, how='left', on=['subject_id', 'time'])

        res = res.drop('charttime', axis=1)
        return res
    

    """
        functionality similar to {merge_feature_to_time_dataframe}, but weight features are recorded based on duration
        need different ways of processing and merging
    """
    def merge_weight_to_time_dataframe(self, cohort_with_time:pd.DataFrame, weight_feature:pd.DataFrame, cohort_df:pd.DataFrame, agg:str):
        cohort = cohort_df[['subject_id', 'episode_id']]
        # filter out the weight feature that not belongs to current cohort
        feature_df = cohort.merge(weight_feature, how='inner', on='subject_id')

        res = cohort_with_time.merge(feature_df, how='inner', on=['subject_id', 'episode_id'])
        # match each time step to weight durations
        res = res.loc[res['time'].between(res['starttime'], res['endtime'])]
        res = res.groupby(by=['episode_id', 'time']).agg(agg)
        res = cohort_with_time.merge(res, how='left', on=['subject_id', 'time'])
        res = res.drop(['starttime', 'endtime'], axis = 1)
        return res


    """
        functionality similar to {merge_feature_to_time_dataframe}, but height features are less frequently recorded
        need different ways of processing and merging
    """
    def merge_height_to_time_dataframe(self, cohort_with_time:pd.DataFrame, height_feature:pd.DataFrame, cohort_df:pd.DataFrame, agg:str):
        feature_df = cohort_df.merge(height_feature, how='inner', on='subject_id')
        # filter out the height features that measured outside ICU stay
        # but lots of subjects only have one height measurement, usually 3-5 minutes before ICU starttime
        # extend the window by 5 minutes to include more height features
        feature_df = feature_df.loc[(feature_df['charttime'] >= (feature_df['starttime'] - pd.Timedelta(5, 'm'))) & (feature_df['charttime'] <= feature_df['endtime'])]
        feature_df = feature_df.drop(['starttime', 'endtime'], axis=1)

        res = cohort_with_time.merge(feature_df, how='left', on=['subject_id', 'episode_id'])
        res = res.drop('charttime', axis=1)
        return res


    '''
        functionality similar to {merge_feature_to_time_dataframe}, but used to merge action/reward into time series cohort
        @param: {action_reward} a task_df for reinforcement learning task. ie. VancomycinDosing.task_df
    '''
    def merge_action_to_time_dataframe(self, cohort_with_time:pd.DataFrame, action_reward:pd.DataFrame, agg:str, time_step:int):
        res = cohort_with_time.merge(action_reward, how='inner', on=['subject_id', 'episode_id'])
        # match each action/reward to its closest time step by charttime
        res = res.loc[(res['charttime'] >= res['time'] - pd.Timedelta(time_step, 'h')) & (res['charttime'] <= res['time'] )]
        # if multiple match, only take last one
        res = res.groupby(by=['episode_id', 'time']).agg(agg)
        res = cohort_with_time.merge(res, how='left', on=['subject_id', 'episode_id', 'time'])
        res = res.drop('charttime', axis=1)
        return res



# a Vancomycin Dosing Prediction Task object
# have a create method to create df
# have a save method to save final df
class VancomycinDosingDataProcessor(BaseDataProcessor):
    def __init__(self):
        super(VancomycinDosingDataProcessor, self).__init__()
        self.cohort_name = "vancomycin_cohort"
        vancomycin_cohort = read_cohort_data(self.cohort_name, self.csv_dir)
        task_label, vancomycin_dose = read_cohort_task('vancomycin_dose', self.cohort_name, self.csv_dir)
        task_label, vancomycin_level = read_cohort_task('vancomycin_level',self.cohort_name, self.csv_dir)

        vancomycin_dose['dose_due'] = vancomycin_dose.apply(lambda x : 0 if x['event_txt'] == 'Hold Dose' else x['dose_due'], axis=1)
        vancomycin_cohort = vancomycin_cohort.drop('los', axis=1)
        self.cohort_df = vancomycin_cohort.sort_values(by=['subject_id'], axis=0).reset_index().drop('index', axis=1)
        self.vancomycin_dose = vancomycin_dose
        self.vancomycin_level = vancomycin_level


    '''
        create the task dataframe for vancomycin dosing reinforcement learning task
    '''
    def create_task_df(self, time_step:int, agg:str)->pd.DataFrame:
        vancomycin_dose = self.vancomycin_dose
        vancomycin_level = self.vancomycin_level

        vancomycin_dose = vancomycin_dose.drop(['dose_given', 'dose_given_unit', 'medication'], axis=1)

        vancomycin_dose.rename(columns={'dose_due':'action'}, inplace=True)
        vancomycin_level.rename(columns={'vancomycin_level':'reward'}, inplace=True)

        # concat dose and measure tables together, then sort based on charttime
        task_df = pd.concat([vancomycin_dose, vancomycin_level])
        task_df = task_df.sort_values(by=['subject_id', 'charttime', 'dose_num'], axis=0)
        task_df = task_df.reset_index().drop('index', axis=1)
        self.task_df = task_df[['subject_id', 'episode_id', 'charttime', 'dose_num', 'action', 'reward']]

        # use the glucose from the vitalsign table instead of chemistry
        self.chemistry_feature = self.chemistry_feature.drop('glucose', axis=1)
        # merge all features together with task_df
        cohort_with_time = self.create_time_cohort(self.cohort_df, time_step)

        feature_table = {
            'chemistry':self.chemistry_feature, 
            'coagulation':self.coagulation_feature, 
            'vitalsign':self.vitalsign_feature,
            'blood':self.blood_feature, 
            'height':self.height_feature, 
            'weight':self.weight_feature
            }
        
        processed_list = []

        for name, feature in feature_table.items():
            if name == 'height':
                temp = self.merge_height_to_time_dataframe(cohort_with_time, feature, self.cohort_df, agg)
            elif name == 'weight':
                temp = self.merge_weight_to_time_dataframe(cohort_with_time, feature, self.cohort_df, agg)
            else:
                temp = self.merge_feature_to_time_dataframe(cohort_with_time, feature, self.cohort_df, agg, time_step)
            processed_list.append(temp)

        action_reward_cohort = self.merge_action_to_time_dataframe(cohort_with_time, self.task_df, agg, time_step)
        processed_list.append(action_reward_cohort)

        for i in range(1, len(processed_list)):
            processed_list[0] = processed_list[0].merge(processed_list[i], how='left', on=['subject_id', 'episode_id', 'time'])

        self.featured_cohort_with_time = processed_list[0]
    

    '''
        automatically save the task dataframe to the given directory in .csv.gz format for later reuse
    '''
    def save_task_df(self, csv_dir:Path, filename:str):
        if 'csv.gz' not in filename:
            raise Exception(f"desired filename with extension .csv.gz, not {filename}")
        
        save_path = csv_dir / filename
        self.featured_cohort_with_time.to_csv(save_path, index=False, compression="gzip")


class HeparinDosingDataProcessor(BaseDataProcessor):
    def __init__(self):
        super(HeparinDosingDataProcessor, self).__init__()
        self.cohort_name = 'heparin_cohort'
        self.cohort_df = read_cohort_data(self.cohort_name, self.csv_dir).drop('los', axis=1)

        task_label, heparin_dose = read_cohort_task('heparin_dose', self.cohort_name, self.csv_dir)
        heparin_dose = heparin_dose.drop(['dose_given', 'dose_given_unit', 'medication', 'starttime', 'endtime', 'los'], axis=1)
        # set the dose amount to 0 for the 'Hold Dose' case
        heparin_dose['dose_due'] = heparin_dose.apply(lambda x : 0 if x['event_txt'] == 'Hold Dose' else x['dose_due'], axis=1)
        self.heparin_dose = heparin_dose.sort_values(by=['subject_id', 'dose_num'], axis=0).reset_index(drop=True)

        heparin_level = self.coagulation_feature.drop(['pt', 'ptt'], axis=1)
        heparin_level = self.cohort_df.merge(heparin_level, how='left', on=['subject_id'])
        # filter out the measurements that are outside of current ICU stay
        heparin_level = heparin_level.loc[(heparin_level['charttime'] > heparin_level['starttime']) & (heparin_level['charttime'] < heparin_level['endtime'])]
        self.heparin_level = heparin_level.drop(['starttime', 'endtime'], axis=1)
    

    def create_task_df(self, time_step:int, agg:str):
        heparin_dose = self.heparin_dose
        heparin_level = self.heparin_level

        heparin_dose.rename(columns={'dose_due':'action'}, inplace=True)
        heparin_level.rename(columns={'inr':'reward'}, inplace=True)

        # concat dose and measure tables together, then sort based on charttime
        task_df = pd.concat([heparin_dose, heparin_level])
        task_df = task_df.sort_values(by=['subject_id', 'charttime', 'dose_num'], axis=0)
        task_df = task_df.reset_index(drop=True)

        # sperate Bolus dose and Infusion dose into two different actions
        task_df['administration_type'] = task_df['administration_type'].apply(lambda x : None if isinstance(x, type(np.nan)) else x)
        task_df['administration_type'] = task_df['administration_type'].apply(lambda x : 'None' if isinstance(x, type(None)) else x)

        task_df['action_bolus'] = task_df.loc[task_df['administration_type'].str.contains('Bolus|Maintenance')]['action']
        task_df['action_infusion'] = task_df.loc[task_df['administration_type'].str.contains('Infusion')]['action']
        self.task_df = task_df.drop(['administration_type', 'action', 'dose_due_unit', 'event_txt'], axis=1)

        # use the glucose from the vitalsign table instead of chemistry
        self.chemistry_feature = self.chemistry_feature.drop('glucose', axis=1)
        # merge all features together with task_df
        cohort_with_time = self.create_time_cohort(self.cohort_df, time_step)

        feature_table = {
            'chemistry':self.chemistry_feature, 
            # 'coagulation':self.coagulation_feature, 
            'vitalsign':self.vitalsign_feature,
            'blood':self.blood_feature, 
            'height':self.height_feature, 
            'weight':self.weight_feature
            }

        processed_list = []

        for name, feature in feature_table.items():
            if name == 'height':
                temp = self.merge_height_to_time_dataframe(cohort_with_time, feature, self.cohort_df, agg)
            elif name == 'weight':
                temp = self.merge_weight_to_time_dataframe(cohort_with_time, feature, self.cohort_df, agg)
            else:
                temp = self.merge_feature_to_time_dataframe(cohort_with_time, feature, self.cohort_df, agg, time_step)
            processed_list.append(temp)

        action_reward_cohort = self.merge_action_to_time_dataframe(cohort_with_time, self.task_df, agg, time_step)
        processed_list.append(action_reward_cohort)
        self.temp = processed_list.copy()

        for i in range(1, len(processed_list)):
            processed_list[0] = processed_list[0].merge(processed_list[i], how='left', on=['subject_id', 'episode_id', 'time'])

        self.featured_cohort_with_time = processed_list[0]


    def save_task_df(self, csv_dir:Path, filename:str):
        if 'csv.gz' not in filename:
            raise Exception(f"desired filename with extension .csv.gz, not {filename}")
        
        save_path = csv_dir / filename
        self.featured_cohort_with_time.to_csv(save_path, index=False, compression="gzip")