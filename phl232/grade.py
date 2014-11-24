'''

Functions for HW10

'''

import pandas as pd
import numpy as np


# Function for Q5, returns a df with [index = Date, Columns =  Rating]
def getGradeCountByTime(df, boro):
    
    if boro == 'NYC':
        pivoted = df.pivot('GRADE DATE', 'CAMIS', 'GRADE')
    else:    
        pivoted = df[df['BORO'] == boro].pivot('GRADE DATE', 'CAMIS', 'GRADE')
    
    pivoted = pivoted.ffill()
    outDF = pivoted.apply(pd.Series.value_counts, axis=1)
    
    return outDF
    
# Function for Q3
def test_grades(grade_list):
# TODO add checks for singleton list and invalid inputs

    
    # This might be the same as just comparing first and last values
    
    if len(grade_list) == 1:
        
        return np.NaN
    
    letterNumDict = dict(zip(list('ABC'), [3,2,1]))
    ratingsNumeric = np.array([letterNumDict[x] for x in grade_list])
    
    ratingsChange = ratingsNumeric[1:] - ratingsNumeric[0:-1]
        
    averageChange = np.mean(ratingsChange)
    
    return np.sign(averageChange)

# Helper Function to get reviews by restaurant ID
def getReviewsByID(data, camis_id):
    
    outData = data.loc[camis_id]    
    
    if outData.ndim == 1:
        return outData
    else:
        return outData.sort(columns = 'GRADE DATE', ascending = True)    

# Function for Q3        
def test_restaurant_grades(data, camis_id):
# Get change by ID

    idGrades = getReviewsByID(data, camis_id)
    
    if idGrades.ndim == 1:
        out = np.NaN
    else:        
        sortedGrades = idGrades['GRADE'].values
        out = test_grades(sortedGrades) 
        
    return out
