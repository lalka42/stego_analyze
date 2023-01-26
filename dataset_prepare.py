import pandas as pd
import numpy as np
import os
from variable import variable
from dump_parser import parser
def dataset_prepare():
 outpath = variable.prepare_set_save_path + '/dataset.xlsx'
 dump_file = os.getcwd() + '\\prepareset.csv'
 parser(variable.prepare_set_path, dump_file)
 df = pd.read_csv(dump_file)
 df['ip.dst'].replace('', np.nan, inplace=True)
 df.dropna(subset=['ip.dst'], inplace=True)
 df.replace(np.nan, 0, inplace=True)
 df['ip.id'] = df['ip.id'].map(lambda x: int(str(x), 16))
 df.to_excel(outpath)