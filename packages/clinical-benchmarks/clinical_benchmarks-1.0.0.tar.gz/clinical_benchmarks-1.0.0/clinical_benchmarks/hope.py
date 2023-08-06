from task import VancomycinDosingDataProcessor
import pandas as pd
from IPython.display import display
import os
from pathlib import Path
import dotenv

env_file = 'D:/UT_Third_Year/2022_Summer/Benchmark_Dataset/clinical-benchmarks/environment_config.env'
dotenv.load_dotenv(env_file, override=True)

print('start creating vanco object')
vanco = VancomycinDosingDataProcessor()
print('vanco object created')

time_step = 4
agg = 'last'
print('start creating vanco task_df')
vanco.create_task_df(time_step, agg)
print('done')