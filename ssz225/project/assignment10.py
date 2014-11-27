import pandas as pd
import matplotlib.pyplot as plt
from project.functions import *

def main():
    """This program is designed to clean and analyze the restaurant grades data 
    (NYC_Restaurant_Inspection_Results) from the NYC DOHMH. 
    The results drawn using citywide and borough-wide data are: 
    graphs of the distribution of A, B, and C's over the years,
    net improvements in participating restaurants,
    distribution ."""

    #import dataset 
    df = pd.read_csv('NYC_Restaurant_Inspection_Results.csv')
    #remove NaNs
    df = df.dropna()
    #filter to only relevant columns
    df = df[['CAMIS', 'BORO', 'GRADE', 'GRADE DATE', 'CUISINE DESCRIPTION']]
    #filter to only entries with valid grades
    grades = df[(df.GRADE == 'A')|(df.GRADE == 'B')|(df.GRADE == 'C')]
#      
#     #Question 4. print and compute sum of test_restaurant_grades for all restaurant
    sum_all = 0
    unique_CAMIS = grades.CAMIS.unique()
    for CAMIS in unique_CAMIS:
        sum_all = sum_all + test_restaurant_grades(CAMIS, grades)
    print 'Sum of test_restaurant_grades for all restaurants is: ' + str(sum_all)
    graph_nyc = graph(grades, 'nyc')
#  
#       
    #print and compute sum of test_restaurant_grades for each borough
    boro = ['MANHATTAN','QUEENS','BROOKLYN','STATEN ISLAND','BRONX']
    for borough in boro:
        sum_boro = 0
        boro_df = grades[grades.BORO == borough]
        unique_CAMIS = boro_df.CAMIS.unique()
        for CAMIS in unique_CAMIS:
            sum_boro = sum_boro + test_restaurant_grades(CAMIS, boro_df)
        graph(boro_df, '{}'.format(borough))
        print 'The sum of test_restaurant_grades for all restaurants in ' + borough + ' is: ' + str(sum_boro)
       


if __name__=='__main__':
    main()