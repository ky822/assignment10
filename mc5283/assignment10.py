import pandas as pd
import numpy as np
from sklearn import linear_model
from supportingFunctions import *


def main():
    df = cleanData()
    
    '''
    question5: plot the grade change with time. I counted the number of
    different grades in each year, from 2010 to 2014, and ploted a 
    stacked pie chart
    '''
    years = []
    for item in df['GRADE DATE']:
        year = item.split('/')[2]
        years.append(year)
    df['YEAR'] = np.array(years)
    
    for boro in df['BORO'].unique():
        dfBoro = df[df.BORO == boro]
        df1 = dfBoro.groupby(['YEAR','GRADE']).size().unstack()
        plotPdf(boro, df1)
    dfNYC = df.groupby(['YEAR', 'GRADE']).size().unstack()
    plotPdf('NYC', dfNYC)

    '''
    question6: I use this data to see the proportion of different cuisine
    types in NYC
    '''
    df2 = df['CUISINE DESCRIPTION']
    counts = df2.value_counts()
    top = counts[:10]
    others = sum(counts[10:])
    top1 = top.append(pd.Series(others, index = ['Others']))
    index = [x.decode('utf8').encode('ascii', 'replace') for x in top1.keys()]
    total_num = sum(counts)
    plt.figure()
    plt.pie(top1/total_num, labels = index, autopct = '%1.1f%%')
    plt.axis('equal')
    plt.savefig('pie chart,png')
if __name__ == '__main__':
    main()


