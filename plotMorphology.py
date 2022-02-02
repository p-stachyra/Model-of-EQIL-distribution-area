#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 21:04:57 2022

@author: jaimylai
"""

import seaborn as sns
import os
import pandas as pd

sns.set()

def visualize_csv(folder):
    """
    To visualise the csv files in dir created into a plot and saves them into a png
    
    """
    
    for filename in os.listdir(folder):
        df = pd.read_csv(folder + '/' + filename)
        df.drop(columns=['Unnamed: 0'], inplace = True)
        plot = sns.displot(df, kind="kde")

        if not os.path.isdir("visualizations"):
            os.mkdir("visualizations")
        plot.savefig("visualizations/"+ filename[:-4]+".png")
        
    return 0