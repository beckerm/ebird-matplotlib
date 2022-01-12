#!/usr/bin/env python3

# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import argparse

png_filename = 'dark_eyed_junco.png'
region_notation = ' - San Francisco Region'

parser = argparse.ArgumentParser(
    description='eBird data plotting.')
parser.add_argument(
    '-f', '--file', help='eBird data file.', required=True)

args = parser.parse_args()

data_file = args.file


rcParams.update({'figure.autolayout': True})
plt.rcParams['axes.linewidth'] = 0.1


df = pd.read_csv(data_file, sep='\t', low_memory=False)

bird_name = df['COMMON NAME'].unique()

df['OBSERVATION DATE'] = pd.to_datetime(
    df['OBSERVATION DATE'], format='%Y-%m-%d')

filtered_df = df.loc[(df['OBSERVATION DATE'] >= '2010-01-01')]

filtered_df_2 = filtered_df.copy()

filtered_df_2['OBSERVATION YEAR'] = pd.DatetimeIndex(
    filtered_df['OBSERVATION DATE']).year

observers_df = filtered_df_2[['OBSERVATION YEAR', 'OBSERVER ID']]

observers_grouped = observers_df.groupby(['OBSERVATION YEAR', 'OBSERVER ID']).count(
).reset_index().groupby('OBSERVATION YEAR').count()


counts_df = filtered_df_2[['OBSERVATION YEAR', 'OBSERVATION COUNT']]

counts_df_2 = counts_df.copy()

counts_df_2['OBSERVATION COUNT'] = pd.to_numeric(
    counts_df['OBSERVATION COUNT'], errors='coerce')


signtings = counts_df_2.groupby('OBSERVATION YEAR')[
    'OBSERVATION COUNT'].sum().astype(int)


final = observers_grouped.merge(signtings, on='OBSERVATION YEAR').plot(
    kind='bar', edgecolor='none', color=['#5cb85c', '#d9534f'], rot=45)


for p in final.patches:
    final.annotate(str(p.get_height()), (p.get_x()
                                         * 1.000, p.get_height() * 1.008))

    # final.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))


final.grid(visible=True, color='grey', linestyle='-', linewidth=0.5, alpha=0.2)
final.set_title(bird_name[0] + region_notation)
final.legend(["Birders", "Observations"],
             bbox_to_anchor=(0.4, 1), frameon=False)
final.spines['top'].set_visible(False)
final.spines['right'].set_visible(False)
final.spines['bottom'].set_linewidth(0.5)
final.spines['left'].set_linewidth(0.5)
final.figure.savefig(png_filename, pad_inches=4.0)
