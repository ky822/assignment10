from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_boro(df,boro):
    '''
    here is a plot function to plot the grade for each boro
    based on the time and GRADE
    
    the plot set is based date, so we need find the grade for each date
    '''
    # group by data
    df_date=df.groupby('Date')
    # create a empty dictionary
    freqs_date={'date':[],'freqs':[]}
    for date,group in df_date:
        dates=group.set_index('Date')
        dates=dates.ix[date]
        date_grade=list(dates.GRADE)
        # use counter function to find the number of each Grade in each date
        freqs = Counter(date_grade)
        #freqs=list(freqs)
        #freqs=list(freqs.items())
        freqs_date['date'].append(date)
        freqs_date['freqs'].append(freqs)
    #make the dictionary to dateframe to make it plot easily
    df_grade=pd.DataFrame.from_dict(freqs_date['freqs'], orient='columns', dtype=None)
    df_date=pd.DataFrame.from_dict(freqs_date['date'])
    df_date_grade=df_date.join(df_grade)
    #re name the columns
    df_date_grade.columns=['Date','A','B','C']
    #
    df_date_grade=df_date_grade.set_index('Date')
        
    
    plt.figure()
    #plot each grade with each color
    plt.plot(df_date_grade.index,df_date_grade['A'],'r-', label = 'A')
    plt.plot(df_date_grade.index,df_date_grade['B'],'g-', label = 'B')
    plt.plot(df_date_grade.index,df_date_grade['C'],'y-', label = 'C')
    plt.title('Number of restaurants in '+ boro + ' each grade')
    plt.ylabel("# of restaurants")
    #save the fig
    plt.savefig('grade_improvement_ ' + boro + ' .pdf')
    