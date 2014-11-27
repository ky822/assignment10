# -*- coding: utf-8 -*-
"""Additional Analysis
   Mengfei Li
"""

__all__=['top_n_cuisine','n_cuisine_name_graph','grade_cuisine','sum_grade_cuisine','n_cuisine_grade']


import collections
import operator
import matplotlib.pyplot as plt
import numpy as np




def top_n_cuisine(dat,n):
    """Given the dataset, return the n most popular(high freq) cuisine type
       over all boroughts and its corresponding count
    """
    c=dict(collections.Counter(dat['CUISINE DESCRIPTION']))
    sort_c=sorted(c.items(),key=operator.itemgetter(1),reverse=True)
    n_most_name=[sort_c[i][0] for i in range(n)]  
   
    return n_most_name, [sort_c[i][1] for i in range(n)]    
    
    
def n_cuisine_name_graph(n,n_most_name,n_values):
    """Plot the frequency barplot of n most popular cuisines.
    """
    ind=np.arange(n)    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    plt.bar(ind,n_values,color='g')
    ax.set_xticks(ind)
    xtickNames=ax.set_xticklabels(n_most_name)
    ax.set_ylabel('cuisine freq')
    ax.set_title('Most '+str(n)+' freq cuisines')
    ax.set_xticklabels(n_most_name,rotation=90)
    plt.setp(xtickNames, rotation=90, fontsize=9)
    plt.show()    
    
    
    
    
def grade_cuisine(cuisine_df):
    """Accept a dataframe which aims for a specific cuisine.
       Return three values that represent
       percentage of each grade in total
    """
    A_grade=len(cuisine_df.GRADE.iloc[np.where(cuisine_df.GRADE=='A')])
    B_grade=len(cuisine_df.GRADE.iloc[np.where(cuisine_df.GRADE=='B')])
    C_grade=len(cuisine_df.GRADE.iloc[np.where(cuisine_df.GRADE=='C')])
    res=sum([A_grade,B_grade,C_grade])  
    
    return A_grade/float(res),B_grade/float(res),C_grade/float(res)
    
    
    
    
def sum_grade_cuisine(dataset):
    """Evaluate the sum grade for different cuisine type over time
       return a list which contains the calculated result for each 
       cuisine
    """
    g_dict_A={}
    g_dict_B={}
    g_dict_C={}
    
    cuisine=np.unique(dataset['CUISINE DESCRIPTION'])
    for ind in range(len(cuisine)):
        cuisine_df=dataset.iloc[np.where(dataset['CUISINE DESCRIPTION']==cuisine[ind])]
        g_dict_A[cuisine[ind]], g_dict_B[cuisine[ind]], g_dict_C[cuisine[ind]]=grade_cuisine(cuisine_df)
        
     
    return g_dict_A, g_dict_B, g_dict_C    
    
    
    
    
def n_cuisine_grade(grade,n_most_name,n):     
    """Plot the percentage grade graph of n most popular cuisines.
    """    
    ind=np.arange(n)    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    plt.bar(ind,grade,color='r')
    plt.legend(loc="upper right")
    ax.set_xticks(ind)
    xtickNames=ax.set_xticklabels(n_most_name)
    ax.set_ylabel('Grade percentage')
    ax.set_title('Most '+str(n)+' freq cuisines\' grade')
    ax.set_xticklabels(n_most_name,rotation=90)
    plt.setp(xtickNames, rotation=90, fontsize=9)
    plt.show()