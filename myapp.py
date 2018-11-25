# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 12:01:08 2018

@author: jjone
"""

# This is the part 3 of cosmetic recommendation: Building a recommendation app using bokeh
# You can also daownload the csv file from same repository: cosmetic.csv


import pandas as pd

from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.layouts import widgetbox, column


df = pd.read_csv('cosmetic_svd.csv')

option_1 = ['Moisturizer', 'Cleanser', 'Treatment', 'Face Mask', 'Eye cream', 'Sun protect']
option_2 = ['Combination', 'Dry', 'Normal', 'Oily', 'Sensitive']


source = ColumnDataSource(df)
plot = figure()
plot.circle(x = 'SVD1', y = 'SVD2', source = source, size = 8, color = 'DarkMagenta')

hover = HoverTool(tooltips = [
        ('Item', '@name'),
        ('brand', '@brand'),
        ('Price', '$ @price'),
        ('Rank', '@rank')])
plot.add_tools(hover)

## defining the callback
def update_plot(attr, old, new):
    a = select_1.value
    b = select_2.value
    a_b = a + '_' + b
    new_data = {
        'x' : df[df['Label'] == a_b]['SVD1'],
        'y' : df[df['Label'] == a_b]['SVD2'],
        'name' : df[df['Label'] == a_b]['name'],
        'brand' : df[df['Label'] == a_b]['brand'],
        'price' : df[df['Label'] == a_b]['price'],
        'rank' : df[df['Label'] == a_b]['rank'],
    }
    source.data = new_data

## adding a dropdown Select widget
select_1 = Select(title = 'Choose the cosmtic category', options = option_1, value = option_1[0])
select_2 = Select(title = 'Choose your skin type', options = option_2, value = option_2[0])

select_1.on_change('value', update_plot)
select_2.on_change('value', update_plot)

layout = column(widgetbox(select_1, select_2), plot)
curdoc().add_root(layout)
curdoc().title = 'CosmeticMap'

# 4. Adding a searching widget
