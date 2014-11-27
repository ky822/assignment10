# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 21:14:54 2014

@author: Israel
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas import DataFrame, Series

#### Asssignment 10, Israel Malkin (im965)

#### Question 2

#load data
data=pd.read_csv('nyc_data.csv',sep=',',header=0)
data['GRADE DATE'] = pd.to_datetime(data['GRADE DATE'])

#cleanup and sort data
clean = data[data.GRADE.isin(['A','B','C'])]
clean = clean[clean.BORO.isin(['Missing'])==0]
clean = clean.drop_duplicates(subset=['CAMIS','GRADE DATE'])
clean = clean.sort_index(by=['CAMIS','GRADE DATE'])
clean['year'] = pd.DatetimeIndex(clean['GRADE DATE']).year

#### Question 3
def test_grades(gradesinput):
    '''Takes a sorted list of alphabetical grades (capitalized)
    and returns 1 if grades have improved,0 if stayed the same, -1 if worsened.
    If list is less than 2 elements, nan is returned
    
    Improvement is measured by comparing the first and last grades'''
    print gradesinput
    if len(gradesinput)<2:
        print "List with less than 2 grades returned a NaN"
        return np.nan
    elif str(gradesinput[-1])<str(gradesinput[0]):
        return 1.0
    elif str(gradesinput[-1])==str(gradesinput[0]):
        return 0.0
    else:
        return -1.0

#### Question 4
def test_restaurant_grades(camis_id, frame=clean):
    '''Takes CAMIS (id) as input and return improve/same/worsened in terms of grades'''
    return test_grades(list(clean[clean.CAMIS==camis_id]['GRADE']))

progress=DataFrame(clean.CAMIS.value_counts(),columns=['Progress'])

for i in clean.CAMIS.value_counts().index:
    progress.ix[i]=test_restaurant_grades(i,frame=clean)
progress['status']=np.nan
progress.loc[progress.Progress==-1,'status']='Worsened'    
progress.loc[progress.Progress==0,'status']='No Change'
progress.loc[progress.Progress==1,'status']='Improved'

#plot of progress
plt.plot()
progress.status.value_counts().plot(kind='bar')
plt.title('Progress of Restaurants in NYC since 2010')
plt.ylabel('# of Restaurants')
plt.xlabel('Status')
plt.savefig('grade_tests_nyc.pdf')
plt.close()



#### Question 5

# Entire City
plt.plot()
clean.GRADE.groupby(clean.year).value_counts().plot(kind='bar')
plt.title('# of Restaurants in NYC by grade across time')
plt.ylabel('# of Restaurants')
plt.xlabel('Labeled as (year, grade)')
plt.savefig('grade_improvement_nyc.pdf')
plt.close()

# By Borough
label={'MANHATTAN':'manhattan','BROOKLYN':'brooklyn','BRONX':'bronx','QUEENS':'queens','STATEN ISLAND':'staten'}
for b in clean.BORO.value_counts().index:
    plt.plot()
    clean[clean.BORO==b].GRADE.groupby(clean.year).value_counts().plot(kind='bar')
    plt.title('# of Restaurants in '+str(b)+' by grade across time')
    plt.ylabel('# of Restaurants')
    plt.xlabel('Labeled as (year, grade)')
    plt.savefig('grade_imporvement_'+label[b]+'.pdf')
    plt.close()
    
    

    

#### Question 6

# I include a file answers.txt which includes the justification for 
# calculating if a restaurant improved or not, and the answer to question 6.

#Below I generate charts used for answering questions 6

#share of resturant with each grade
clean['one']=1
by_grade = DataFrame(clean.groupby([clean.year,clean.GRADE]).one.sum())
total = DataFrame(clean.groupby([clean.year]).one.sum())
merged = pd.merge(by_grade,total,right_index=True,left_index=True)
share = 100*merged.one_x/merged.one_y

plt.plot()
share.plot(kind='bar')
plt.title('Grade Proportion in NYC across time')
plt.ylabel('Share of Restaurants')
plt.xlabel('Labeled as (year, grade)')
plt.savefig('grade_shares_nyc.pdf')
plt.close()


#### Plot by Country (Italian and Chinese)
types=['Chinese','Italian']
top=clean[clean['CUISINE DESCRIPTION'].isin(types)]
groups=top[['CUISINE DESCRIPTION','GRADE']].groupby('CUISINE DESCRIPTION')
plt.plot()
groups.GRADE.value_counts().plot(kind='bar')
plt.title('Grades By Cuisine Type')
plt.ylabel('# of Restaurants')
plt.xlabel('Labeled as (Cuisine Type, grade)')
plt.savefig('grade_by_type.pdf')
plt.close()


    
    
    
    
        


