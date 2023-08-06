import argparse
import os
import sys
import logging
import pandas as pd
import logging
from pathlib import Path

from clinical_benchmarks.model import predict_task
from clinical_benchmarks.extract import (
    check_bq_components, run_queries, copy_from_bq_to_bucket, download_gcs_file
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S'
)
logger = logging.getLogger(__name__)


class EnvDefault(argparse.Action):
    """Argument parser class which inherits from environment and has a default value."""
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault,
              self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def dir_path(string):
    return Path(string)


def parse_arguments(arguments=None):
    """Parse input arguments for entry points."""
    parser = argparse.ArgumentParser(
        description="clinical-benchmarks command line interface"
    )
    parser.add_argument(
        '--csv_dir',
        required=True,
        action=EnvDefault,
        envvar='MODEL_DIR',
        default='csv/',
        type=dir_path,
        help='Directory with CSV tables'
    )

    subparsers = parser.add_subparsers(dest="actions", title="actions")
    subparsers.required = True

    # Downloading
    filter_download = subparsers.add_parser(
        "download", help=("Download options for cohort data")
    )
    filter_download.add_argument(
        '--project',
        action=EnvDefault,
        envvar='GCP_PROJECT',
        required=True,
        help='Google Cloud project'
    )
    filter_download.add_argument(
        '--dataset',
        action=EnvDefault,
        envvar='BQ_DATASET',
        required=True,
        help='BigQuery dataset for creation of tables'
    )
    filter_download.add_argument(
        '--bucket',
        action=EnvDefault,
        envvar='GCS_BUCKET',
        required=True,
        help='Google Cloud Storage bucket for downloading data'
    )
    filter_download.add_argument(
        '--mimic_derived',
        action='store_true',
        help='Downloads all the mimic_derived variable tables'
    )

    # Data filtering options
    filter_opt = subparsers.add_parser(
        "model", help=("Model filtering options for cohort data")
    )

    filter_opt.add_argument(
        '--task',
        choices=['mortality', 'los_icu', 'dialysis', 'inv_vent'],
        required=True
    )
    filter_opt.add_argument(
        '--los',
        type=float,
        default=1,
        dest='filter_los',
        help='LOS measured in fractional days'
    )
    filter_opt.add_argument(
        '--start_time',
        type=float,
        default=0,
        dest='filter_start_time',
        help='Start time units are fractional days'
    )
    filter_opt.add_argument(
        '--stop_time',
        type=float,
        default=1,
        dest='filter_stop_time',
        help='Stop time units are fractional days'
    )

    filter_opt.add_argument(
        '--model_type', default='lr', choices=['lr', 'xgb'], dest='model_type'
    )

    return parser.parse_args(arguments)


def download(args):
    """Run queries on BigQuery to generate datasets, copy data to GCS, then download locally."""
    check_bq_components(args.project, args.dataset, args.bucket)
    run_queries(args.project, args.dataset)

    download_file_list = [
        'cohort.csv.gz', 'vancomycin_cohort.csv.gz', 'chemistry.csv.gz',
        'coagulation.csv.gz', 'complete_blood_count.csv.gz',
        'weight.csv.gz','height.csv.gz', 'vitalsign.csv.gz',
        'vancomycin_dose.csv.gz', 'vancomycin_level.csv.gz',
        'labevents.csv.gz', 'mortality.csv.gz', 'los_icu.csv.gz',
        'inv_vent.csv.gz', 'dialysis.csv.gz', 'heparin_cohort.csv.gz',
        'heparin_dose.csv.gz'
    ]
    for f in download_file_list:
        copy_from_bq_to_bucket(f, args.project, args.dataset, args.bucket)
        download_gcs_file(f, args.csv_dir, args.project, args.bucket)

    if args.mimic_derived:
        full_variable_list = [
            'age', 'antibiotic', 'bg', 'blood_differential', 'cardiac_marker',
            'charlson', 'chemistry', 'coagulation', 'complete_blood_count',
            'crrt', 'dobutamine', 'enzyme', 'epinephrine', 'gcs', 'height',
            'icp', 'inflammation', 'norepinephrine', 'oxygen_delivery',
            'phenylephrine', 'rhythm', 'rrt', 'suspicion_of_infection',
            'urine_output', 'vasopressin', 'ventilation', 'ventilator_setting',
            'vitalsign', 'weight_durations'
        ]
        var_dir = args.csv_dir / 'variables'
        for var in full_variable_list:
            f = f'{var}.csv.gz'
            copy_from_bq_to_bucket(f, args.project, args.dataset, args.bucket)
            download_gcs_file(f, var_dir, args.project, args.bucket)


def main(argv=sys.argv):
    """Entry point for package."""

    args = parse_arguments(argv[1:])

    if args.actions == 'download':
        download(args)
    elif args.actions == 'model':
        if args.filter_start_time > args.filter_stop_time:
            logger.warn("Filter start_time is later than filter stop_time")
        model, y_pred = predict_task(args)
    else:
        logger.warn('Unrecongnized command')


if __name__ == '__main__':
    main()