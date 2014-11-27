import numpy as np
import pandas as pd
from Q3 import test_grades

def test_restaurant_grades(df, camis_id):
    '''
    This function returns the score of a given restaurant.
    '''
    df2 = df.ix[camis_id]
    # If there is only one grade, returns 0
    if len(df2.GRADE) == 1:
        final_score = 0
    else:
        grade_list = df2.sort(columns='GRADE DATE').GRADE #Sort grades by time
        final_score = test_grades(grade_list)
    return final_score

def Run(data):
    print '\n-------------------Answer to question 4 -------------------'
    print 'The function \'test_restaurant_grades(camis_id)\' that Question 4 is asking for can be found in Q4.py\n'
    nyc_grades = 0 # Initializing NYC Grades
    for name in ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']:
        df_tmp = data[data.BORO == name]
        camis_index = list(df_tmp.index.unique())
        score_values = []
        for camis_id in camis_index:
            score_tmp = test_restaurant_grades(df_tmp, camis_id)
            score_values.append(score_tmp)
        nyc_grades += sum(score_values)
        print 'The sum grades of {} is {}.\n'.format(name, sum(score_values))
    print 'The sum grades of NYC is {}.\n'.format(nyc_grades)
