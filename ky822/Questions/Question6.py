'''
Created on Nov 30, 2014

@author: keye
'''
from functions import *
from graphs import GenerateGraph_Question6

def Question6(df):
    #We can figure out the percentage of different kinds of cuisines for NYC restaurants.
    print '----------Questions 6----------\nGenerate a graph to show the percentages of the top 10 cuisines so that we can make a assumption for the favors of customers.'
    df_Cuisine = CleanupData_Question6(df)
    #Generate a pie to show the percentages of the top 10 cuisines for NYC restaurants.
    GenerateGraph_Question6(df_Cuisine)
    print '\nQuestion 6 finished!'
    print '------------------------------------------------'
    
    