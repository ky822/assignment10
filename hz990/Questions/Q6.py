import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
pd.set_option('display.mpl_style', 'default')
import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = (16.0, 10.0)
def Run(data):
    '''Answers to question 6

    '''
    print '\n-------------------Answer to question 6 -------------------'
    print '\nFirst, we can plot the trend of the number of restaurant that had been inspected since 2010.'
    
    def plot_trend(df):
        '''
        This function plots the trend of the number of restaurant that been inspected.

        '''
        # Generating an index of date
        date_index = sorted(list(df['GRADE DATE'].unique())) 
        
        # Generating a list to store the trend values
        num_trend = []
        for date in date_index:
            df1 = df[df['GRADE DATE'] == date]
            number = len(list(df1.index.unique())) # Counting unique restaurant
            num_trend.append(number)

        # Plotting
        df_new = pd.DataFrame(num_trend, index=date_index, columns=['Number of restaurants inspected per day'])
        plt.figure()
        df_new.plot()
        plt.savefig('Trend of Inspected Restaurant Numbers')

    # Calling the function to plot the trend figure
    plot_trend(data)
    print 'This figure has been saved in \'Trend of Inspected Restaurant Numbers.png\''


    print '\nNext, we can generating Pie-charts to show the composition of cuisine in each borough.'
    print 'This figure has been saved in \'Cuisine in each area.png\''
    print '\nThe conclusion for question 6 can be seen in \'conclusion_Q6.txt\'\n'

    def plot_cuisine(df):
        '''
        This functions plots cuisine types in each borough.
        '''
        BOROs = ['NYC', 'BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']
        
        plt.figure()
        for i in range(len(BOROs)):
            if BOROs[i] == 'NYC': # plotting NYC first
                plt.subplot(2, 3, i)
                df['CUISINE DESCRIPTION'].value_counts()[:6].plot(kind='pie', title='NYC')
            else: # plotting each borough
                df_tmp = df[df.BORO == BOROs[i]]
                plt.subplot(2, 3, i)
                df_tmp['CUISINE DESCRIPTION'].value_counts()[:6].plot(kind='pie', title=BOROs[i])
        plt.savefig('Cuisine in each area')
    
    # Calling the function to plot cuisine figure
    plot_cuisine(data) 
