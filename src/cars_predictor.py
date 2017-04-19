import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from utils_pkg import utils

df = pd.read_csv('../res/cars_11_04_2017.tsv', sep='\t')
## Fix Columns...
# PRICE -> REMOVE THE EMPTY SPACES
df['PRICE'] = df['PRICE'].str.replace(' ', '')
df['PRICE'] = df['PRICE'].str.replace('Notpric', '')
df['PRICE'] = pd.to_numeric(df['PRICE'])

# MILEAGE
df['MILEAGE'] = df['MILEAGE'].str.replace(' ', '')
df['MILEAGE'] = df['MILEAGE'].str.replace('km', '')
df['MILEAGE'] = pd.to_numeric(df['MILEAGE'])

# LOCATION
df['LOCATION'] = df['LOCATION'].str.replace(' › Outside Finland', '')

# MODEL -> Splited into BRAND, MODEL_NAME, CC
df['BRAND'] = pd.Series(index=df.index)
df['MODEL_NAME'] = pd.Series(index=df.index)
df['CC'] = pd.Series(index=df.index)

df_split = pd.DataFrame(df['MODEL'].str.split(' \(', 1).tolist(), columns = ['OTHER','CC'])
df_split = pd.DataFrame(df_split['OTHER'].str.split(' ', 1).tolist(), columns = ['BRAND','MODEL_NAME'])
df['BRAND'] = df_split['BRAND']
df['MODEL_NAME'] = df_split['MODEL_NAME']

df_split = pd.DataFrame(df['MODEL'].str.split(' \(', 1).tolist(), columns = ['OTHER','CC'])
df_split = pd.DataFrame(df_split['CC'].str.replace(')', '').tolist(), columns = ['CC'])
df_split['CC'] = pd.to_numeric(df_split['CC'])
df['CC'] = df_split['CC']

# Indexing columns: BRAND, MODEL_NAME, LOCATION, GEAR, ENGINE
df['BRAND_ID'] = utils.get_serie_ids(df['BRAND'])
df['MODEL_NAME_ID'] = utils.get_serie_ids(df['MODEL_NAME'])
df['LOCATION_ID'] = utils.get_serie_ids(df['LOCATION'])
df['GEAR_ID'] = utils.get_serie_ids(df['GEAR'].dropna())
df['ENGINE_ID'] = utils.get_serie_ids(df['ENGINE'].dropna())

# Setting the indexed dataframe
df_indexed = df[['PRICE','YEAR','MILEAGE','ENGINE_ID','GEAR_ID','BRAND_ID','MODEL_NAME_ID','CC','LOCATION_ID']]
df_indexed = df_indexed.dropna()
print('printing plot...')