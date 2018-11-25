# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 00:19:42 2018

@author: jjone
"""

# This is the part 3 of cosmetic recommendation: Building a recommendation app using bokeh
# You can also daownload the csv file from same repository: cosmetic.csv


import pandas as pd
import numpy as np
import re
from sklearn.decomposition import TruncatedSVD

from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import widgetbox, column

# 1. Define a function embedding ingredients and decomposition at once
def my_type(label, skin_type):
    ''' Define a function creating a dataframe for each option '''
    df = cosm_2[cosm_2['Label'] == label][cosm_2[skin_type] == 1]
    df = df.reset_index()

    # embedding each ingredients
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

    # creating dtm matrix
    D = len(corpus)   # number of items
    N = len(word_index_map)   # total number of ingredients
    X = np.zeros((D, N))

    def tokens_to_vector(tokens):
        # initialize empty array
        x = np.zeros(len(word_index_map))
        # vectorize
        for token in tokens:
            i = word_index_map[token]
            x[i] = 1
        return x

    i = 0
    for tokens in corpus:
        X[i, :] = tokens_to_vector(tokens)
        i += 1

    # decomposition using SVD
    svd = TruncatedSVD()
    Z = svd.fit_transform(df_token)

    # conbining into one data frame
    Z_df = pd.DataFrame(data = Z, columns = ['SVD1', 'SVD2'])
    cosm_svd = pd.concat([df.iloc[:, 1:6], Z_df], axis = 1)
    return cosm_svd


# 2. Get the dataframe for all combinations
option_1 = cosm_2.Label.unique().tolist()
option_2 = cosm_2.columns[6:]


option_1 = ['moisturizer']
option_2 = ['Combination', 'Dry']

b = pd.DataFrame()
for label in option_1:
    for skin_type in option_2:            
            a = my_type(label, skin_type) 
            a['Label'] = label + '_' + skin_type
            b.append(a)


moi_dry = my_type('moisturizer', 'Dry')





# 3. Build the interactive bokeh App 
source = ColumnDataSource()
plot = figure(x_range, y_range)
plot.circle(x = 'SVD1', y = 'SVD2', source = source, size = 8, color = 'DarkMagenta')

hover = HoverTool(tooltips = [
        ('Item', '@name'),
        ('brand', '@brand'),
        ('Price', '$ @price'),
        ('Rank', '@rank')])
plot.add_tools(hover)


## defining the callback
def update_plot(attr, old, new):
    a = option_1.value
    b = option_2.value
    a_b = a + '_' + b
    new_data = {
        'x' = df[df['Label'] == a_b]['SVD1'],
        'y' = df[df['Label'] == a_b]['SVD2'],
        name = df[df['Label'] == a_b]['name'],
        brand = df[df['Label'] == a_b]['brand'],
        price = df[df['Label'] == a_b]['price'],
        rank = df[df['Label'] == a_b]['rank'],
    }
    source.data = new_data
    
    
## adding a dropdown Select widget
select_1 = Select(title = 'What items are you looking for?', options = option_1, value = option_1[0])
select_2 = Select(title = 'What is your skin type?', options = option_2, value = option_2[0])

select.on_change('value', update_plot)

layout = column(widgetbox(select_1, select_2), p)
output_file('Cosmetic.html')
curdoc().add_root(layout)


# 4. Adding a searching widget




