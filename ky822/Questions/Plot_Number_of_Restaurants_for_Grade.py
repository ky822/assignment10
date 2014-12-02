'''
Created on Nov 30, 2014

@author: keye
'''

from functions import  *
from graphs import *

def Plot_Number_of_Restaurants_for_Grade(df):
    """
    This function will generate 6 graphs:
    
    1. Generate one graph that shows the total number of restaurants in New York City for each grade over time.
    
    2. Generate one graph for each of the five Boroughs that shows the total number of restaurants in the Borough for each grade over time.
    
    """
    
    #Question5: Gernerate the following six graphs.
    print '----------Questions 5----------\nGenerate the following six graphs according to the Questions 5:\nThis may take a long time... '
    
    #a. Generate a graph that shows the total number of restaurants in New York City for each grade over time.
    GenerateGraph(df,'nyc')
    
    #Put all unique items of the column 'BORO' into a list Boroughs_list. And delete the 'Missing' items.
    Boroughs_list = list(df.BORO.unique())
    Boroughs_list.remove('Missing')
    
    #Generate one graph for each of the five Boroughs that shows the total number of restaurants in the Borough for each grade over time.
    for boro in Boroughs_list:
        df_borough = df[df.BORO==boro]
        GenerateGraph(df_borough,boro.lower())
    
    print '\nQuestion 5 finished!'
    print '------------------------------------------------'