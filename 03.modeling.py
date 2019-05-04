# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 19:56:54 2018

@author: jjone
"""

# This is the part 2 of cosmetic recommendation: analyzing cosmetic items similarities based on their ingredients
# You can also daownload the csv file from same repository: cosmetic.csv


import pandas as pd
import numpy as np
from sklearn.manifold import TSNE


# Load the data
cosm_2 = pd.read_csv('data/cosmetic_p.csv')

# All possible combinations for the option choices
option_1 = cosm_2.Label.unique().tolist()
option_2 = cosm_2.columns[6:].tolist()


## defining a function embedding ingredients and decomposition at once
def my_recommender(op_1, op_2):
    df = cosm_2[cosm_2['Label'] == op_1][cosm_2[op_2] == 1]
    df = df.reset_index()

    # embedding each ingredients
    ingredient_idx = {}
    corpus = []
    idx = 0

    for i in range(len(df)):
        ingreds = df['ingredients'][i]
        ingreds = ingreds.lower()
        tokens = ingreds.split(', ')
        corpus.append(tokens)
        for ingredient in tokens:
            if ingredient not in ingredient_idx:
                ingredient_idx[ingredient] = idx
                idx += 1

    # Get the number of items and tokens
    M = len(df)                 # The number of the items
    N = len(ingredient_idx)     # The number of the ingredients

    # Initialize a matrix of zeros
    A = np.zeros(shape = (M, N))

    # Define the oh_encoder function
    def oh_encoder(tokens):
        x = np.zeros(N)
        for t in tokens:
            # Get the index for each ingredient
            idx = ingredient_idx[t]
            # Put 1 at the corresponding indices
            x[idx] = 1
        return x

    # Make a document-term matrix
    i = 0
    for tokens in corpus:
        A[i, :] = oh_encoder(tokens)
        i += 1

    # Dimension reduction with t-SNE
    model = TSNE(n_components = 2, learning_rate = 200)
    tsne_features = model.fit_transform(A)

    # Make X, Y columns
    df['X'] = tsne_features[:, 0]
    df['Y'] = tsne_features[:, 1]

    return df


# Create the dataframe for all combinations
df_all = pd.DataFrame()
for op_1 in option_1:
    for op_2 in option_2:
            temp = my_recommender(op_1, op_2)
            temp['Label'] = op_1 + '_' + op_2
            df_all = pd.concat([df_all, temp])

# Save the file
df_all.to_csv('data/cosmetic_TSNE.csv', encoding = 'utf-8-sig', index = False)
