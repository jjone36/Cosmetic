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
cosm = pd.read_csv('cosmetic.csv')
cosm.info()

cosm = cosm.loc[pd.notnull(cosm['ingredients'])]
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
a = [t.split('\r\n\r\n') for t in cosm['ingredients']]
pattern = ['\r\n', '-\w+: ', 'Please', 'No Info', 'This product', 'Visit']

for i in range(len(cosm)):
    Num = len(a[i])
    for j in range(Num):
        if all(x not in a[i][j] for x in pattern):
           cosm_2['ingredients'][i] = a[i][j]


# step 2. tokenizing ingredients
cosm_2.head()
cosm_2.columns[6:]

## types: 'Combination', 'Dry', 'Full', 'Light', 'Matte', 'Medium',
##        'Natural', 'Normal', 'Oily', 'Radiant', 'Sensitive'

df = cosm_2[cosm_2['Label'] == 'cleanser'][cosm_2['Oily'] == 1]
df = df.reset_index()

word_index_map = {}
index_word_map = []
current_index = 0
corpus = []

for i in range(len(df)):
    text = df['ingredients'][i]
    text = text.lower()
    tokens = text.split(', ')
    corpus.append(tokens)
    for token in tokens:
        if token not in word_index_map:
            word_index_map[token] = current_index
            current_index += 1
            index_word_map.append(token)

word_index_map['water']
index_word_map[4]

D = len(corpus)   # number of documents
N = len(word_index_map)   # total number of tokens
X = np.zeros((D, N))

def tokens_to_vector(tokens):
    # initialize empty array
    x = np.zeros(len(word_index_map))
    # vectorize
    for token in tokens:
        i = word_index_map[token]
        x[i] = 1
    return x

# document-term matrix
i = 0
for tokens in corpus:
    X[i, :] = tokens_to_vector(tokens)
    i += 1

df_token = pd.DataFrame(data = X, index = df.name, columns = index_word_map)


# step 3. item similarities
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD()
Z = svd.fit_transform(X)

plt.scatter(Z[:, 0], Z[:, 1])
for i in range(D):
    plt.annotate(s = df.name[i], xy = (Z[i, 0], Z[i, 1]))
plt.show()


Z_df = pd.DataFrame(data = Z, columns = ['SVD1', 'SVD2'])
cosm_svd = pd.concat([df.iloc[:, 1:6], Z_df], axis = 1)

cosm_svd['rank'].head()


from bokeh.plotting import figure, ColumnDataSource
from bokeh.io import output_file, show
from bokeh.models import HoverTool

source = ColumnDataSource(cosm_svd)

p = figure()
p.circle(x = 'SVD1', y = 'SVD2', source = source, size = 8, color = 'salmon')

hover = HoverTool(tooltips = [
        ('Item', '@name'),
        ('brand', '@brand'),
        ('Price', '$ @price'),
        ('Rank', '@rank')])

p.add_tools(hover)

show(p)
