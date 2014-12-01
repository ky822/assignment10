'''
Created on Nov 30, 2014

@author: keye
'''
from functions import *

def Question2():
    #Questions 1&2: Import the database into a pandas DataFrame and clean up the data. for example, by removing all entries that have invalid grades (in the 'GRADE' column).
    Raw_NYCRestaurantInspection = LoadData()
    NYCRestaurantInspection = CleanupData(Raw_NYCRestaurantInspection)
    print 'The dataset is loaded and cleaned up.\nQuestion 1&2 finished!'
    print '------------------------------------------------'
    return NYCRestaurantInspection, Raw_NYCRestaurantInspection