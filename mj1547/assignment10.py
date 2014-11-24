'''
Created on Nov 21, 2014

@author: jiminzi
'''

import numpy as np
import pandas as pd
from test_restaurant_grades import test_restaurant_grades
from functions.plot import plot_boro
from functions.format_date import format_date
def main():
    '''
    clean data set
    1) remove invalied grade rows
    2)change the format of column GRADE DATE  to a sortable kind Datw format
    '''
    #import data as dataframe
    data=pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
    data=pd.DataFrame(data)
    #df=data.dropna(subset=['GRADE'])
    # clean the missing data and invalid data
    keep=['A','B','C']
    df_clean=data[data['GRADE'].isin(keep)]
    #convert the GRADE column to list
    list_d=list(df_clean['GRADE DATE'])  
    #change the format of GRADE DATE column to a datetime format for sorting
    x=format_date(list_d)
    df_clean['Date']=x
   
    df_resturant=df_clean.set_index('CAMIS')


    '''
    make the dataframe for each boroughs with the total values
    
    '''
    #group the data set to sevral groups by the colum label boro
    df_boro=df_resturant.groupby('BORO')
    #df_grouped=df_resturant.groupby(level='CAMIS',sort=False)
    #x=0
    print 'Value of each boroughs:'
    #use a double for loop to calculate value for each camis for each boroughs 
    for boroughs,group in df_boro:
        #print boroughs
        df_grouped=group.groupby(level='CAMIS',sort=False)
        x=0
        for CAMIS, groupx in df_grouped:
            #use the test_restaurant_grads function to get value
            x=x+test_restaurant_grades(groupx,CAMIS)
        print boroughs
        print x
    
    '''
    plot 6 each graphs 
    '''
    
    plot_boro(df_clean,'nyc')  
    #change the name of boro values there is do not need missing boro ,so remove
    boro=['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND']
    df_clean_remove_missing=df_clean[df_clean['BORO'].isin(boro)]
    df_rename=df_clean_remove_missing.replace(['BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND'] , ['bronx','brooklyn','manhattan','queens','staten']) 
    #print df_rename
    df_boroughs=df_rename.groupby('BORO')

    # get the value for each boro
    for boroughs,group in df_boroughs:
        plot_boro(group,boroughs)
       
    question6(df_clean)
    
    
def question6(df_clean):   
    '''
    For question 6 ,
    I think this data set can help us to find the most popular cuisine in new york city, based on my test grade functiion, 
    I think we can get the value for each kind of cuisine type, and then find the highest value, which means the most popular
    '''
    print 'Question 6:'
    print ' The value for each type of cuisine:'
    df_resturant=df_clean.set_index('CAMIS')
    #make the data set to many groups by cuisine description
    cuisine_sum=df_resturant.groupby('CUISINE DESCRIPTION')    
    #create a dictionay
    cuisine_dic={'cuisine':[],'value':[]}
    #a double for loop to get the value for each group
    for cuisine,group in cuisine_sum:
        cuisine_dic['cuisine'].append(cuisine)
        df_grouped_cuisine=group.groupby(level='CAMIS',sort=False)
        x=0 
        for CAMIS, groupx in df_grouped_cuisine:
            x=x+test_restaurant_grades(groupx,CAMIS)
            
        cuisine_dic['value'].append(x)
    #convert the dictionary to dataframe 
    df_cuisine=pd.DataFrame.from_dict(cuisine_dic,orient='columns', dtype=None)
    df_s=df_cuisine.sort(['value'],ascending=False)
    # print the data frame of the value for each cuisine type
    print df_s
    #print df_cuisine_value
    print 'By this data frame,and there almost have 84 different kind of cuisines \n I calculate the value for each kind of cuisine, which is the rank of value \n and we canfind the most popular is American, and then is chinese cuisine'
    print 'this data set is useful to assessing the quality of restaurants in NYC, we can find all the value for all boroughs are positive,\n that means generally speaking the quilty for all the restaurant in NYC are improving.'
if __name__ == '__main__':
    main()