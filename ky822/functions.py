'''
Created on Nov 25, 2014

@author: keye
'''

import pandas as pd
import numpy as np
import sys


def LoadData():    
    """
    Input the file path of a certain dataset and load the dataset into a DataFrame and return the DataFrame. 
    """
   
    #Try until a valid file path is input.
    while True:
        try:
            filepath= raw_input('Please enter the file path of the dataset: ')
            DataFrame = pd.read_csv(filepath, low_memory=False)
            break
        except (KeyboardInterrupt,EOFError):
            print 'You are going to exit the program!\nBye!'
            sys.exit()
        except IOError:
            print "The file doesn't exist.\nYour input is not a valid file path. Be careful about the format and spell! Please try again!\n"
    
    return DataFrame 


def CleanupData(df):
    """
    Clean up the data of a dataframe and return a new dataframe.
    """
    
    #Obtain a new dataframe with only 4 columns :'CAMIS','BORO','GRADE' and 'GRADE DATE'.
    df = df[['CAMIS','BORO','GRADE','GRADE DATE']]
    
    #Drop the missing data, the 'Missing' in column 'BORO'and the duplicated data.
    df_withoutNA = df.dropna()
    df_withoutNA = df_withoutNA.drop_duplicates()
    
    #Keep the valid grades, which are 'A', 'B' and 'C' only.
    GradeA,GradeB,GradeC = df_withoutNA.GRADE == 'A',df_withoutNA.GRADE == 'B',df_withoutNA.GRADE == 'C'  
    dfValid_Grade_withoutNA = df_withoutNA[GradeA|GradeB|GradeC]
    
    #Change the data of column 'GRADE DATE' to type of datetime and sort the data by column 'GRADE DATE'.
    dfValid_Grade_withoutNA.loc[:,'GRADE DATE'] = pd.to_datetime(dfValid_Grade_withoutNA.loc[:,'GRADE DATE'])
    dfValid_Grade_withoutNA = dfValid_Grade_withoutNA.sort('GRADE DATE')
    return dfValid_Grade_withoutNA

def CleanupData_Question6(df):
    """
    Clean up the data for Questions 6
    """
    
    #Obtain a new dataframe with only 2 columns : 'CAMIS', 'CUISINE DESCRIPTION'.
    df = df[['CAMIS','CUISINE DESCRIPTION']]
    
    #Drop the missing data and the duplicated camis_id
    df_withoutNA = df.dropna()
    df_withoutNA = df_withoutNA.drop_duplicates(subset='CAMIS')
    
    #Get the count of each unique item in the column 'CUISINE DESCRIPTION'.
    cuisine = pd.value_counts(df_withoutNA['CUISINE DESCRIPTION'].ravel()).index
    
    #Get cuisines whose counts are top 10 and form a new dataframe.
    df_withoutNA_result = df_withoutNA[df_withoutNA['CUISINE DESCRIPTION']==cuisine[0]]
    for i in range(9):
        df_temp = df_withoutNA[df_withoutNA['CUISINE DESCRIPTION']==cuisine[i+1]]
        df_withoutNA_result = df_withoutNA_result.append(df_temp)    
    return df_withoutNA_result
    

def test_grades(grade_list):
    """
    Create a function that takes a list of grades sorted in date order, and returns 1 if the grades are improving, -1 if they are
    declining, or 0 if they have stayed the same.
    """
    grade_value = {'A':3,'B':2,'C':1}
    grade_value_list = []
    grade_value_count = 0
    
    #Turn the grades into grade values which are 3, 2, 1, and put them into a list.
    for grade in grade_list:
        grade_value_list.append(grade_value[grade])
    
    #Check if the previous value of grade for the restaurant is bigger, the count plus -1. If the previous value of grade is smaller, the count plus 1. Else, the count stays the same.
    for i in xrange(len(grade_list)):
        if i==0 or grade_value[grade_list[i]] == grade_value[grade_list[i-1]]:
            grade_value_count += 0
        elif grade_value[grade_list[i]] > grade_value[grade_list[i-1]]:
            grade_value_count += 1
        else:
            grade_value_count -= 1    
    
    #When the count is positive, returns 1. If the count is negative, returns -1. Else, returns 0.
    if grade_value_count>0:
        return 1
    elif grade_value_count<0:
        return -1
    else:
        return 0
       
        
def test_restaurant_grades(df, camis_id):
    """
    Examine if the grades of certain restaurants improve, decline or stay the same over time.
    """
    #Get a list of grades for a certain camis_id and examine if the grades of restaurants improve, decline or stay the same over time.  
    grade_of_restaurant = df.loc[df['CAMIS']==camis_id, 'GRADE'] 
    grade_result = test_grades(list(grade_of_restaurant))  
    return grade_result   


def sum_of_test_grades(df):
    """
    Compute the sum of test_restaurant_grades for all the restaurants.
    """
    #Get all the unique items of column 'CAMIS'.
    unique_CAMIS_id = df['CAMIS'].unique()
    count_values = 0
    
    #Compute the sum of test_restaurant_grades for the unique items.
    for camis_id in unique_CAMIS_id:
        count_value = test_restaurant_grades(df,camis_id)
        count_values  += count_value
    return count_values 
    