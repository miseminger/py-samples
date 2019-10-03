# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 10:19:10 2019

@author: miseminger
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('/Users/miseminger/Documents/celladaptationtracking.xlsx', sheet_name='Sheet1') #reads the whole excel file into memory
df['hours'] = np.nan #add a new column for time in hours to be added, beginning at 0h

#prepare arrays of variables to iterate through
celltypes = df.cell_type.unique()
media = df.medium.unique()

graphsubject = 'viable_cell_concentration'
#graphsubject = 'viable_cell_percentage'


fignum = 1

for c in celltypes:
    for medium in media:
        fig = plt.figure(fignum) #set a figure to be filled for this cell type and media type
        
        
        indices = (df[(df['cell_type'] == str(c)) & (df['medium'] == str(medium))].index).tolist()
        shakeoptions = df.loc[indices, 'shaking'].unique()
        for shake in shakeoptions:
            #make this line below more elegant later
            shakeindices = (df[(df['cell_type'] == str(c)) & (df['medium'] == str(medium)) & (df['shaking'] == shake)].index).tolist()
            #shakeindices = (df.loc[indices]['shaking']==str(shake)).index.tolist()
            passagenums = df.loc[shakeindices, 'passage_from_DMEM'].unique()

            #convert times for each passage to hours starting from 0 when each passage was created
            for passage in passagenums:
                    passageindices = (df[(df['cell_type'] == str(c)) & (df['medium'] == str(medium)) & (df['shaking'] == shake) & (df['passage_from_DMEM'] == passage)].index).tolist()
                    days = df.loc[passageindices, 'date'].tolist()  #list of days for that passage
                    hours = df.loc[passageindices, 'time_nearest_h_ish'].tolist()  #list of hours for that passage        
                    time = np.zeros(len(hours)) #get an empty array to put hours in
                    for i in range(len(hours)): #complete datetime format by adding hours
                        days[i] = days[i].replace(hour=hours[i])
                    for j in range(len(hours)): #get difference between times in hours
                        diff = days[j] - days[0]
                        diffhours = int(diff.total_seconds()//3600)
                        time[j] = int(diffhours)
                    df.loc[passageindices,'hours'] = time #fill in hours in dataframe

                    if shake=='n':
                        shakelabel = 'static'
                        fmtstring = '--o'
                    elif shake=='y':
                        shakelabel = 'shaking'
                        fmtstring = '--o'
                        
                    if graphsubject == 'viable_cell_concentration':
                        plt.errorbar(df.loc[passageindices, 'hours'], df.loc[passageindices, 'viable_cell_concentration'], yerr=df.loc[passageindices, 'stdev'], label=("P" + str(passage) + " " + shakelabel), fmt=fmtstring)
                        plt.ylabel('viable cell concentration (cells/ml)')
                        plt.legend(loc='upper left')
                    elif graphsubject == 'viable_cell_percentage':
                        plt.errorbar(df.loc[passageindices, 'hours'], df.loc[passageindices, 'viable_cell_percentage'], label=("P" + str(passage) + " " + shakelabel), fmt=fmtstring)
                        plt.ylabel('percent viability')
                        plt.legend(loc='lower left')
                        plt.ylim(0,1.1)
                    plt.title(str(c) + " " + str(medium) + " Adaptation")
                    plt.xlabel('time (h)')
                    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
                    figname = '/Users/miseminger/Documents/adaptationplots/' + str(c) + "_" + str(medium) + "_" + graphsubject + ".png"
                    plt.savefig(figname)
                    
        fignum += 1
