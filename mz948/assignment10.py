import pandas as pd
import numpy as np
from supportfunctions import *
import matplotlib.pyplot as plt
from gradeTestFunctions import *
dataFrame = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')

# question 1: clean the data
# drop the row of dataFrame that contains missing value in column 'GRADE'
dataFrame = dataFrame[pd.notnull(dataFrame['GRADE'])]
# drop the row whose grade is not yet graded
dataFrame = dataFrame[dataFrame['GRADE'] != 'Not Yet Graded']
# drop the row whose borough is missing
dataFrame = dataFrame[dataFrame['BORO'] != 'Missing']
#convert the date string to datetime
dataFrame['GRADE DATE'] = pd.to_datetime(dataFrame['GRADE DATE'])

#create a list of boroughs
boroughs = dataFrame['BORO'].unique()

def question4():
    borough_grade = []
    for borough in boroughs:  
        
        df_by_boroughs = dataFrame[dataFrame.BORO == borough]
        each_borough_grade = 0
        borough_id_list = list(df_by_boroughs.CAMIS.drop_duplicates())
       
        for id_nums in borough_id_list:
            each_test_score = test_restaurant_grades(id_nums)        
            each_borough_grade += each_test_score
        borough_grade.append(each_borough_grade)
        
    return borough_grade

#question 5 
grade_type =dataFrame['GRADE'].unique()
#print grade_type   

def question5b():
    '''
    Generates a graph that shows the total number of restaurants in different 
    boroughs for each letter grade over time.
    '''
    #create the data frame of different boroughs and plot them
    for borough in boroughs:    
        grade_plot(dataFrame[dataFrame.BORO == borough], borough.lower().split(' ')[0])

def main():
    borough_grade_list = question4()
    overall_sum = np.sum(borough_grade_list)
    print "The overall sum of of the test grades of restaurants in NYC is " + str(overall_sum)+"."
    #Generates a graph that shows the total number of restaurants in New York City 
    #for each grade over time
    grade_plot(dataFrame,'nyc')
    
    for i in range(len(borough_grade_list)):
        print '{}:{}'.format(boroughs[i], borough_grade_list[i])
    
    question5b()
    
if __name__ == '__main__':
    main()
