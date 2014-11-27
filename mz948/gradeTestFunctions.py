import numpy as np
import pandas as pd
from supportfunctions import *

dataFrame = pd.read_csv('restaurant grade.csv')

# question 1: clean the data
# drop the row of dataFrame that contains missing value in column 'GRADE'
dataFrame = dataFrame[pd.notnull(dataFrame['GRADE'])]
# drop the row whose grade is not yet graded
dataFrame = dataFrame[dataFrame['GRADE'] != 'Not Yet Graded']
# drop the row whose borough is missing
dataFrame = dataFrame[dataFrame['BORO'] != 'Missing']
#convert the date string to datetime
dataFrame['GRADE DATE'] = pd.to_datetime(dataFrame['GRADE DATE'])

# question 3
def test_grades(grade_list):
    '''
    takes a list of grades (e.g. [A, B, C, B]) sorted in date order, and 
    returns 1 if the grades are improving, -1 if they are declining, or 0 if 
    they have stayed the same.
    '''
    grade_list = grade_list_transform(grade_list)
    splitIndex = len(grade_list)/2
    if splitIndex == 0:
        #when there is only one grade for the restaurant, I assume that the 
        #the score has not change
        return 0 
    
    else:
        #calculate the averages of the first half of grades and the second half of grades 
        avgFirstHalf = np.mean(grade_list[0:splitIndex])
        avgSecondHalf = np.mean(grade_list[splitIndex:])
        if avgFirstHalf < avgSecondHalf:
            return 1
        elif avgFirstHalf == avgSecondHalf:
            return 0
        else:
            return -1

def test_restaurant_grades(camis_id):
    '''This function takes a camis id as argument and returns the restaurant's grade'''
    grade_by_id = list(dataFrame.loc[dataFrame['CAMIS'] ==camis_id, 'GRADE'])
    test_score = test_grades(grade_by_id)
    return test_score 
      
