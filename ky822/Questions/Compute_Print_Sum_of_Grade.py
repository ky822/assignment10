'''
Created on Nov 30, 2014

@author: keye
'''
from functions import *

def Compute_Print_Sum_of_Grade(df):
    """
    This function is to solve Questions 4:
    Write the function called test_restaurant_grades(camis_id) to examine if the grades improve, decline or stay the same over time. 
    Compute and print out the sum of test_restaurant_grades(camis_id) over all restaurants and for each of the five Boroughs.
    """
     
    print '----------Questions 4----------\nCompute the sum of test_restaurant_grades(camis_id) over all restaurants in the dataset and for each of the five Boroughs.\nPrint out these value:\n\nThis may take some time...'
        
    #Compute the sum of test_testaurants(camis_id) over all restaurants in the dataset and print out the value.
    sum_of_all_restaurants = sum_of_test_grades(df)
    result_overall = '\nThe sum of grades for all restaurants is {}'.format(sum_of_all_restaurants)
    print result_overall
    
    #Open a file to save the result.
    f = open('results_of_question4.txt','a+')
    f.write(result_overall+'\n')
    
    #Put all unique items of the column 'BORO' into a list Boroughs_list. And delete the 'Missing' items.
    Boroughs_list = list(df.BORO.unique())
    Boroughs_list.remove('Missing')
    
    #Compute the sum of test_testaurants(camis_id) for each of the five Boroughs and print out the values. 
    for boro in Boroughs_list:
        df_borough = df.loc[df.BORO==boro]
        sum_of_grades = sum_of_test_grades(df_borough)
        result = 'The sum of test_restaurant_grades for all the restaurants in {} is {}'.format(boro,sum_of_grades)
        print result
        #Write the result into the file 'results_of_question4.txt'.
        f.write(result+'\n')
    f.close()
    
    print '\nQuestion 4 finished!'
    print '------------------------------------------------'
    