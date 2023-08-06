# clinical-benchmarks
A comprehensive set of clinical benchmarks

## Installation

* **(Recommended)** Create the `benchmark` environment: `conda env create -f environment.yml`
* Pip install: `pip install clinical_benchmarks`

## Usage

### Regenerate data files

If you'd like to regenerate the data files from the source datasets, you'll need to have a Google Cloud Platform (GCP) account, BigQuery dataset, and GCS storage bucket prepared. These are used to (1) create intermediate tables, (2) copy those tables out of BigQuery to GCS, and finally (3) download the tables locally.

As described by the [Python Client for Google BigQuery](https://googleapis.dev/python/bigquery/latest/index.html), setup requires you to:

* [Select or create a Cloud Platform project.](https://console.cloud.google.com/project)
* [Enable billing for your project.](https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project)
* [Enable the Google Cloud BigQuery API.](https://cloud.google.com/bigquery)
* [Setup Authentication.](https://googleapis.dev/python/google-api-core/latest/auth.html)

Once you have GCP project, have created a BigQuery dataset, and have created a GCP storage bucket, you can use environment variables to specify them when running the download script:

```sh
export GCP_PROJECT='MY-GCP-PROJECT'
export BQ_DATASET='MY-BIGQUERY-DATASET'
export GCS_BUCKET='MY-STORAGE-BUCKET'
export MODEL_DIR='MY-SAVE-DIR'
clinical_benchmarks download
```

**If you are not a Linux/MacOS user**
Alternatively, you can specify the values at the command line:

```sh
clinical_benchmarks --csv_dir MY-SAVE-DIR download --project MY-GCP-PROJECT --dataset MY-BIGQUERY-DATASET --bucket MY-STORAGE-BUCKET
```

If you prefer to mannually regenerate the data files
Check the data_pipeline.ipynb which prepared runnable cells to download data files

### Create task dependent datasets
#### Available Tasks
	- Vancoymydin Dosing Prediction (Reinforcement Learning)
	- Heparin Dosing Prediction (Reinforcement Learning)

All tasks are designed as data processing class, inherited from the BaseDataProcessor class.
Each task class has two methods, **create_task_df** and **save_task_df**. (detail see task.py)

#### Procedure of creating task datasets
(check data_pipeline.ipynb for runnable example)
1. Modify the **environment_config.env** file with your own environment variables
2. Import necessary packages and use **dotenv** to load **environment_config.env**
   	```python3
	import dotenv
	env_file = 'path_to_environment.env'
	dotenv.load_dotenv(env_file, override=True)
	```
3. Choose a task, such as Vancomycin dosing prediction.
4. Create the task object.
    ```python3
    vanco = VancomycinDosingDataProcessor()
    ```
5. Create task dataframe by calling method **create_task_df**. This method require two arguments, **time_step** and **agg**. 
**time_step** determines the time interval (hourly based) between each state, and **agg** determines the aggregation method that will be used during dataframe merging process, such as "last". 
    ```python3
	time_step = 4
	agg = 'last'
    vanco.create_task_df(time_step, agg)
	# featured_cohort_with_time is the outcome task_df
	display(vanco.featured_cohort_with_time)
    ```
6. Save the task dataframe created in step 5 to a given directory by calling method **save_task_df**. This method require two arguments, **csv_dir** and **filename**. 
**csv_dir** needs to be a Path object, which specify the directory you would like to save the task_df, and **filename** is a str that represent the output file name (the filename must has a .csv.gz extension).
    ```python3
	csv_dir = Path('YOUR_SAVE_DIR')
	filename = 'vancomycin_dosing_task.csv.gz'
	# will save vanco.featured_cohort_with_time as a .csv.gz file
	vanco.save_task_df(save_dir, filename)
    ```
7. Check your saving directory, and try it with your model!