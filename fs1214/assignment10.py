'''
Created on 2014.11.19

@author: apple
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.cm as cm
from functions import *

def question4(df):
    #question4 a: compute the sum of test_restaurant_grades(camis_id) over all restaurants in NYC.
    
    print 'Question 4'
    print 'Please be patient. It will take a while.'
    #Get a list of unique values of CAMIS
    unique_id = list(set(df.index))
    #Set the result 'total' an initial value 0.
    total = 0
    for i in unique_id:
        total = total + test_restaurant_grades(df, i)
    output_string = 'The sum of grade changes over all the restaurants in NYC is {}'.format(total)
    print output_string
    
    #Save the output into a file named answers.txt.
    f = open('answers.txt','w')
    f.write('Question4: \n')   
    f.write('{} \n'.format(output_string))
    
    #question4 b:compute the sum of test_restaurant_grades(camis_id) for each of the five Boroughs.
    
    #Get a list of unique values of BORO. The list has 'Missing', remove this.
    boroughs = list(set(df.BORO))
    boroughs.remove('Missing')
    #Save the borough and the result of each borough in the dictionary.
    boro_dict = {}
    for boro in boroughs:
        grade_boro = df[df['BORO']==boro]
        unique_id = list(set(grade_boro.index))
        total = 0
        for i in unique_id:
            total = total + test_restaurant_grades(grade_boro, i)
        boro_dict[boro] = total
        output_string = 'The sum of grade changes over all the restaurants in {} is {}'.format(boro,total)
        print output_string
        f.write('{} \n'.format(output_string))
    f.write('\n')
    f.close()
    print '------------------'
    
def question5(df):   
    #question5 a
    grade_plot(df,'nyc')
    
    #question5 b: Get the boroughs from BORO column. Plot he total number of restaurants in each borough.
    boroughs = list(set(df.BORO))
    boroughs.remove('Missing')
    for boro in boroughs:
        grade_boro = df[df['BORO']==boro]
        grade_plot(grade_boro,boro.lower().split(' ')[0])
    
    f = open('answers.txt','a')
    f.write('Question5: \n')   
    f.write('These are six graphs as the question asked.\n'
            'From these graphs, we could say the curves in each graph are similar.\n'
            '1.In all areas, most of restaurants get the grade of A, a small amount of restaurants have B or C.\n'
            '2.The number of restaurants having A has been increasing all the time, and between 2012 and 2013 it increased very fast.\n'
            '3.The number of restaurants having B or C has been very flat, although between 2012 and 2013 the number of restaurants having B increased a little.\n'
            '4.Among these boroughs, the number of restaurants having A in manhattan is the largest, and then in brooklyn,queen,bronx,staten island.\n')
    f.write('\n')
    f.close()

"""
In the question6, we need to clean the data again in a different way. 
We keep 'CAMIS', 'BORO', 'CUISINE DESCRIPTION' columns.
We can get the ratio of every kind of restaurant in all the restaurants in NYC,
assessing the quality of restaurants.
"""
def question6(filename):
    #clean the data
    newdf = cleandata_6(filename)
    
    pie_plot(newdf)
    grade_cuisine_plot(newdf)
    
    f = open('answers.txt','a')
    f.write('Question6: \n')   
    f.write('I found the information about CUISINE DESCRIPTION is also very useful.\n'
            '1.From the pie chart, we can compare the percentage of top 10 types restaurants.\n'
            '  The top 10 types restaurants are: American, Chinese, Pizza,Italian, Latin,Cafe/Coffee/Tea,Mexican, Japanese, Bakery, Caribbean etc.\n'
            '2.From another plot chart, we can compare the grade in these top 10 types restaurants.\n'
            '  The restaurants which have the best grade are America, and then Chinese, Pizza,Italian, Latin,Cafe/Coffee/Tea,Mexican, Japanese, Bakery, Caribbean etc,\n'
            '  In general, the grades of these restaurants have been increasing, and the quality of NYC restaurants in different types is getting better.')
    f.write('\n')
    f.close()

def main():
    filename = 'DOHMH_New_York_City_Restaurant_Inspection_Results.csv'
    print 'Please be patient. It will take a while.'
    cleandf = cleandata(filename)
    
    question4(cleandf)
    question5(cleandf)
    question6(filename)
    
    print 'End'

if __name__ == '__main__':
    main()