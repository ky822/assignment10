from get_improvement import *
from data_cleaning import *
from graphs import *
import pandas as pd
import numpy as np


def main():
    '''
    Main program that generates answers for assginment 10.
    Read the data, clean the data, calculate the sum of restarurant improvements in NYC and boroughs.
    Plot the number of 3 grades in NYC and boroughs over time.
    Create a bar plot for the number of restaurants in different cuisines.
    '''
    
    #Q2:
    results = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv') #import the dataset into a data frame called results
    cleaned_data = clean_data_q2(results)


    #Q4 & Q5:
    cleaned_data_sorted = cleaned_data.sort('GRADE DATE')# sort the data frame by date in an ascending order
    city_sum = get_sum(cleaned_data_sorted)#q4: sum for the city
    print 'Q4: The sum over all restaurants in the city is {}'.format(city_sum)
    
    date_grade_id_df = process_data_q5(cleaned_data_sorted)
    grade_graph(date_grade_id_df,'NYC')#q5: graph for the city

    collect_boroughs = ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']
    for borough in collect_boroughs:
        borough_df = cleaned_data_sorted[cleaned_data_sorted['BORO'] == borough]  
        borough_sum = get_sum(borough_df)#q4: sum for the boroughs
        print '{} sum is {}'.format(borough, borough_sum)
        
        boro_date_grade_id_df = process_data_q5(borough_df)
        grade_graph(boro_date_grade_id_df,borough)#q5:graph for the boroughs

        
    #Q6:
    data_q6 = process_data_q6(results)    
    selector_data_q6 = selector(data_q6,1000)#select cuisines that have more than 1000 restaurants.
    bar_grade(selector_data_q6)
    
    
if __name__=='__main__':
    main()