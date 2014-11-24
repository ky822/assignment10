# -*- coding: utf-8 -*-
"""Assignment 10
   Mengfei Li
"""

__all__=['scale_grade','test_grade','test_restaurant_grades','g_date','grade_over_time','total_grade','grade_boro']

import pandas as pd
import numpy as np
import datetime
import collections


def scale_grade(grade_list):
    """Valid input should be a list that has any kind of combination of 
       ('A','B','C') and encode 'A' as 3, 'B' as 2, 'C' as 1
       Return the modified grade_list
    """
    for ind, grade in enumerate(grade_list):
        if grade=='A':
           grade_list[ind]=3
        elif grade=='B':
           grade_list[ind]=2
        else:
            grade_list[ind]=1
        
    return grade_list

def test_grade(grade_list):
    """Valid input should be a sorted list according to the grade date
       that contains grades over the period for a certain restaurant.
       Function returns a single value that indicates the change of grades 
    """
    num_grade=scale_grade(grade_list)
    trend=[]
    for ind in range(len(num_grade)-1):
        if num_grade[ind+1]>num_grade[ind]:
            trend.append(1)
        elif num_grade[ind+1]<num_grade[ind]:
            trend.append(-1)
        else:
            trend.append(0)
        
    if sum(trend)>0:
        return 1
    elif sum(trend)<0:
        return -1
    else:
        return 0

def test_restaurant_grades(dataset,camis_id):
    """Accpet dataset to evaluate and ID for restaurant. After implementation,
       return the improvment result over time for this restaurant. 
    """
    #get grades and date for a specified camis_id as g
    g=dataset.GRADE.iloc[np.where(dataset.CAMIS==camis_id)]  
    date=dataset['GRADE DATE'].iloc[np.where(dataset.CAMIS==camis_id)]
    date=pd.Series([datetime.datetime.strptime(d,"%m/%d/%Y") for d in date],index=g.index,name='GRADE DATE')
    g_date=pd.concat([g,date],axis=1)
    #sort grade according to date
    g_date=g_date.sort(columns='GRADE DATE',axis=0)   
    
    return test_grade(list(g_date.GRADE))
    
    
    

def g_date(data):
    """Accept a dataset to be analysis and create a new dataframe 
       which contains only date (year category) and
       grade for each year (2010,2011,2012,2013,2014)
    """    
    #pull out data from the most original dataset and modified the date by year
    g=data.GRADE
    date=data['GRADE DATE'] 
    date=[datetime.datetime.strptime(d, "%m/%d/%Y") for d in date]

    d_by_year=[]  
    for i in range(len(date)):        
        d_by_year.append(datetime.datetime(date[i].year,1,1))

    d_by_year=pd.Series(d_by_year,index=g.index,name="GRADE DATE")
    return pd.concat([g,d_by_year],axis=1)



def grade_over_time(g_date):   
    """Modified the g_date dataframe and return with the grade_frequency
       with respect to each year
    """
    year_df=g_date.groupby('GRADE DATE')['GRADE']
    gradeOverTime={}
    for name, group in year_df:
        gradeOverTime[name]=collections.Counter(group)

    gradeOverTime=pd.DataFrame(gradeOverTime)
    gradeOverTime=pd.DataFrame(gradeOverTime.values.T,columns=gradeOverTime.index,index=[2010,2011,2012,2013,2014])
    

    return gradeOverTime

        
    
        


def total_grade(df):
    """Given a dataset to access, return the sum of result over all grades 
       received in this dataset.
    """
    unique_id=set(df.CAMIS)
    total=0
    for elem in unique_id:
        total=total+test_restaurant_grades(df,elem)
        
    return total
    
    
    
def grade_boro(boroughts,data):
    """Evaluate the total grade with respect to each boro
       Return the sum of result.
    """
    boro_df=data.iloc[np.where(data.BORO==boroughts)]
    return total_grade(boro_df)
    
    
 
    
    
    



    