# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 19:56:54 2018

@author: jjone
"""

# This is the part 2 of cosmetic recommendation: analyzing cosmetic items similarities based on their ingredients
# You can also daownload the csv file from same repository: cosmetic.csv


import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

# step 1. cleaning data
cosm = pd.read_csv('data/cosmetic.csv')
cosm.info()

cosm = cosm.loc[pd.notnull(cosm['Ingredients'])]
cosm.info()

# label
cosm.Label[cosm['Label'] == 'moisturizing-cream-oils-mists'] = str('Moisturizer')
cosm.Label[cosm['Label'] == 'cleanser'] = str('Cleanser')
cosm.Label[cosm['Label'] == 'facial-treatments'] = str('Treatment')
cosm.Label[cosm['Label'] == 'face-mask'] = str('Face Mask')
cosm.Label[cosm['Label'] == 'eye-treatment-dark-circle-treatment'] = str('Eye cream')
cosm.Label[cosm['Label'] == 'sunscreen-sun-protection'] = str('Sun protect')

# name -> duplicated item
df_2 = cosm['name'].drop_duplicates()
cosm = cosm.loc[df_2.index, :].reset_index()

# URL
cosm.drop(['URL', 'index'], axis = 1, inplace = True)

# price
pattern = re.compile(r"(\d+).\d+")
for i in range(len(cosm)):
    cosm['price'][i] = re.findall(pattern, cosm['price'][i])[0]

cosm['price'] = pd.to_numeric(cosm['price'])

# rank
cosm['rank'].fillna(0, inplace = True)
cosm.info()

# skin_type
pattern = re.compile(r"([a-zA-Z]+)\\n")
for i in range(len(cosm)):
    cosm['skin_type'][i] = re.findall(pattern, cosm['skin_type'][i])

## list column dummies
df_2 = cosm['skin_type'].str.join('|').str.get_dummies()
cosm_2 = cosm.join(df_2).drop('skin_type', axis = 1)

## tokenize ingredients
a = [t.split('\r\n\r\n') for t in cosm['Ingredients']]
pattern = ['\r\n', '-\w+: ', 'Please', 'No Info', 'This product', 'Visit']

for i in range(len(cosm)):
    Num = len(a[i])
    for j in range(Num):
        if all(x not in a[i][j] for x in pattern):
           cosm_2['Ingredients'][i] = a[i][j]

# save the file
df.to_csv('data/cosmetic_p.csv', encoding = 'utf-8-sig', index = False)
