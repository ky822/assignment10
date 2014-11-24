import pandas as pd
import numpy as np

df = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
#remove the rows that have invalid grades or other invalid features
df = df.dropna()
df = df[df['GRADE'] != 'Not Yet Graded']
df = df.drop_duplicates()

def test_grades(grade_list):
    if len(grade_list) == 0:
        return 0
    else:
        if len(grade_list)%2 == 0:
            midpoint = len(grade_list)/2
        else:
            midpoint = (len(grade_list)+1)/2
    
    numeric_list = []
    for grade in grade_list:
        grade = grade.lower()
        number = ord(grade) - 96
        numeric_list.append(number)
    
    first_half_mean = np.mean(numeric_list[:midpoint-1])
    second_half_mean = np.mean(numeric_list[midpoint:])
    
    if first_half_mean < second_half_mean:
        return 1
    elif first_half_mean == second_half_mean:
        return 0
    else:
        return -1

def test_restaurant_grades(camis_id):
    grade_list = list(df.loc[df['CAMIS'] == camis_id, 'GRADE'])
    restaurant_grade = test_grades(grade_list)
    return restaurant_grade

