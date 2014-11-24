from supplement import clean_data, plot_nyc, test_restaurant_grades
import numpy as np
import matplotlib.pyplot as plt

def main():
    """
    main program that will generate the results
    """
    df=clean_data()  # load in cleaned data
    plot_nyc(df)  # plot the graph for the entire NYC
    plt.title('Total Number of restaurants in NYC for each grade over time')  # add plot attributes
    plt.ylabel('Restaurant counts')
    plt.savefig('grade_improvement_NYC.pdf')
    print 'Generating plots for NYC'
    
    borough=df['BORO'].unique().tolist()  # load five boroughs into a list
    
    for i in borough:  # plot graph on each borough in the boroughs list
        plot_nyc(df[df['BORO']==i])
        plt.title('Total Number of restaurants in %s for each grade over time' % i)  # add plot attributes
        plt.ylabel('Restaurant counts')
        plt.savefig('grade_improvement_%s.pdf' % i)
        print 'Generating plots for %s' % i
    
    CAMIS_list=df['CAMIS'].unique().tolist()  # find all unique camis_id in the data set
 
    result=[]  # initialize a empty list to store the return value of grade test for each restaurant    
    for i in CAMIS_list:
        returned=test_restaurant_grades(i, df)  # returned value for each CAMIS ID
        result.append(returned)  # store returned value for each restaurant
    print 'NYC:%s' % np.sum(result)  # print out the sum

    for i in borough:
        borough_df=df[df['BORO']==i]  # subset the dataframe to each given borough
        borough_CAMIS_list=borough_df['CAMIS'].unique().tolist()  # find all unique CAMIS ID in this borough 
        borough_result = []  # initialize a empty list to store return value of grade test
        for j in borough_CAMIS_list:
            returned=test_restaurant_grades(j, borough_df)  # returned value for each CAMIS ID
            borough_result.append(returned)  # store returned value for each restaurant
        print '%s:%s' %(i, np.sum(borough_result))  # print out the sum consecutively
    
if __name__=='__main__':
    main()


	
