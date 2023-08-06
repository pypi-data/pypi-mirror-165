# Generate the tables from BQ through python
import os
import sys
from importlib.resources import open_text
from google.cloud import storage, bigquery
from google.cloud.exceptions import NotFound, Forbidden, BadRequest
import logging
from pathlib import Path

import clinical_benchmarks

logger = logging.getLogger(__name__)


def check_bq_components(project, dataset, bucket_name):
    """ Check BQ components exists and error if they do not"""
    client_bq = bigquery.Client(project=project)
    try:
        client_bq.get_dataset(f'{project}.{dataset}')
    except BadRequest:
        logger.error(f'Project {project} not found')
    except NotFound:
        logger.error(f'Dataset {dataset} is not found in project {project}')

    client_storarge = storage.Client(project=project)
    bucket = client_storarge.bucket(bucket_name)
    try:
        bucket.exists()
    except BadRequest:
        logger.error(f'Bucket {bucket_name} does not exist')
    except Forbidden:
        logger.error(f'You do not have access to Bucket {bucket_name}')


def run_queries(project, dataset):
    """Run queries and output to a specified BigQuery dataset."""
    # Construct a BigQuery client object.
    client = bigquery.Client(project=project)

    # all pre-written SQL query in the qeury folder
    query_locations = [
        ['clinical_benchmarks.query.mimic', 'cohort.sql'],
        ['clinical_benchmarks.query.mimic.task_cohort', 'vancomycin_cohort.sql'],
        ['clinical_benchmarks.query.mimic.task_cohort', 'heparin_cohort.sql'],
        ['clinical_benchmarks.query.mimic.feature', 'chemistry.sql'],
        ['clinical_benchmarks.query.mimic.feature', 'coagulation.sql'],
        ['clinical_benchmarks.query.mimic.feature', 'complete_blood_count.sql'],
        ['clinical_benchmarks.query.mimic.feature', 'height.sql'],
        ['clinical_benchmarks.query.mimic.feature', 'weight.sql'],
        ['clinical_benchmarks.query.mimic.feature', 'vitalsign.sql'],
        ['clinical_benchmarks.query.mimic.outcome', 'vancomycin_dose.sql'],
        ['clinical_benchmarks.query.mimic.outcome', 'vancomycin_level.sql'],
        ['clinical_benchmarks.query.mimic.outcome', 'labevents.sql'],
        ['clinical_benchmarks.query.mimic.outcome', 'mortality.sql'],
        ['clinical_benchmarks.query.mimic.outcome', 'los_icu.sql'],
        ['clinical_benchmarks.query.mimic.outcome', 'dialysis.sql'],
        ['clinical_benchmarks.query.mimic.outcome', 'inv_vent.sql'],
        ['clinical_benchmarks.query.mimic.outcome', 'heparin_dose.sql']
    ]

    for module, query_name in query_locations:
        with open_text(module, query_name) as fp:
            query = ''.join(fp.readlines())

        query_stem = query_name.split('.')[0]
        table_name = f'{project}.{dataset}.{query_stem}'

        logger.info('Generating tables: ' + query_stem)
        # Overwrite table if exists (may remove this)
        job_config = bigquery.QueryJobConfig(
            destination=table_name, write_disposition='WRITE_TRUNCATE'
        )

        # call API to create the table
        query_job = client.query(query, job_config=job_config)
        # wait for the job to complete
        query_job.result()


def copy_from_bq_to_bucket(filename, project, dataset, bucket):
    """Copy a table from BigQuery to a bucket."""
    client = bigquery.Client(project=project)

    destination_uri = f'gs://{bucket}/{filename}'
    dataset = bigquery.DatasetReference(project, dataset)
    table = dataset.table(filename.split('.')[0])

    # extract gzip compressed CSV files
    config = bigquery.job.ExtractJobConfig(
        compression='gzip', destination_format='csv'
    )
    extract_job = client.extract_table(
        table, destination_uri, location="US", job_config=config
    )

    # wait for job to complete
    extract_job.result()
    logger.info(f'Created {destination_uri}')


def download_gcs_file(filename, csv_dir:Path, project, bucket_name='data-benchmark'):
    logger.info(f'Downloading: {filename}')
    file_path = csv_dir / filename
    client = storage.Client(project=project)
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(filename)
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    blob.download_to_filename(file_path)
