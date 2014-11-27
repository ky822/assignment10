import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utility import load_data
from utility import clean_data
from utility import test_grades
from utility import test_restaurant_grades
from utility import df_reference

#Functions for question 4

#This function is to calculate the sum of test_grade for all restaurants in nyc and in each boroughs
def grade_sum(df):
    
    """
    Return:
    sum_nyc: int, sum of test_grade in nyc
    sum_boro: pandas.series, sum of test_grade for each boroughs
    """
    
    #calculate test_grade score for all restaurants
    score = []
    for camis_id in df.index.unique():
        grade = test_restaurant_grades(df, camis_id)
        score.append(grade)

    #build a dataframe with restaurant ID, boroughs and test_grade score for all restaurant
    score_df = pd.DataFrame(score)
    score_df = score_df.set_index(df.index.unique())
    df_refer = df_reference(df)
    score_df['BORO'] = df_refer['BORO']
    score_df.columns = ['increase', 'BORO']
    
    sum_nyc = score_df['increase'].sum() #sum test_grade for all restaurants in nyc
    sum_boro = score_df.groupby('BORO')['increase'].sum() #sum test_grade in each boroughs
    sum_boro = sum_boro.drop('Missing')
    
    return sum_nyc, sum_boro

#Functions for question 5

#This function is to count the number of restaurants for each grade overtime
def grade_count_overtime(df):
    
    """
    Return:
    grade_overtime_df: a result dataframe with the number of restaurants in each grade overtime
    """
    df_sorted=df.sort(columns='GRADE DATE') #sort datafrmae by date order
    previous_grade = {} #a dictionary to store restaurant ID and their grade
    date = df_sorted.iloc[0]['GRADE DATE'] #set a start date
    count = {'A':0,'B':0,'C':0} #a dictionary to store number of restaurants for each grade
    a_total = [] #a list to store number of A restaurants in each date
    b_total = [] #a list to store number of B restaurants in each date
    c_total = [] #a list to store number of C restaurants in each date
    
    for i in xrange(0,len(df_sorted.index)):
        index = df_sorted.index[i]
        
        if df_sorted.iloc[i]['GRADE DATE'] != date: #if current date is not previous date
            date = df_sorted.iloc[i]['GRADE DATE'] #change current date to be the reference date
            a_total.append(count['A']) #store previous count results in corresponding list
            b_total.append(count['B'])
            c_total.append(count['C'])
        
        if index in previous_grade: #if the restaurant was counted before, erase its previous grade
            count[previous_grade[index]] -= 1
    
        count[df_sorted.iloc[i]['GRADE']] += 1   
        previous_grade[index] = df_sorted.iloc[i]['GRADE']
    
    a_total.append(count['A']) #store the last result
    b_total.append(count['B'])
    c_total.append(count['C'])
    
    #build a dataframe to store the number of restaurants in each grade overtime
    grade_overtime_df = pd.DataFrame([a_total, b_total, c_total]).T
    grade_overtime_df.columns = ['A','B','C']
    grade_overtime_df.index = df_sorted['GRADE DATE'].unique()
    
    return grade_overtime_df

#This function is to plot the number of restaurants in each grade overtime
def grade_overtime_plot(df, title):
    """
    title: the title of the plot, like 'nyc', 'manhattan', etc.
    
    Note: this function will save the plot as a pdf file
    """
    grade_overtime_df = grade_count_overtime(df)
    grade_overtime_df.plot()
    plt.title('Grade number over time in {}'.format(title))
    plt.savefig('results/grade_improvement_{}.pdf'.format(title))

#Functions for question 6

def get_top_10_nyc(df):
    """
    Return: a numpy array, names of top 10 types of restaurant in NYC
    Note: the function will save the result in bar plot as a .png file
    """
    df = df.drop_duplicates() #drop duplicates
    df = df.dropna() #drop missing data
    restaurants_type = df['CUISINE DESCRIPTION'].value_counts()
    restaurants_type_df = pd.DataFrame(restaurants_type)
    restaurants_type_df = restaurants_type_df.drop('Other') #drop the restaurant type 'Other'
    top_10_nyc = restaurants_type_df.head(10) #get the top 10 restaurant types in nyc
    #reset top 10 restaurant type names into a readable form
    top_10_name = ['American','Chinese','Coffee/Tea','Pizza','Italian','Latin','Japanese','Mexican','Bakery','Caribbean']
    top_10_nyc['Type'] = top_10_name
    top_10_nyc.columns = ['Count', 'Type']
    top_10_nyc = top_10_nyc.set_index('Type')
    top_10_nyc = top_10_nyc.sort(columns='Count') #sort by numbers of restaurant in each type
    
    #plot a bar to show the result
    top_10_nyc.plot(kind = 'barh', alpha = 0.7, color = 'Aquamarine', legend = False, title = 'Top 10 types of restaurants in NYC')
    plt.savefig('results/Top_10_restaurant_types_in_NYC.png')
    return restaurants_type_df.head(10).index.unique()

#This function is to calculate grade amounts and overall scores for each restaurant type overtime
def top_10_grade_overtime(df, type_name):
    
    """
    type_name: array or list, name of top 10 restaurant types
    
    Return:
    df_sum: a result dataframe which shows the overall score for each restaurant type overtime
    """
    
    df_res_name = df[df['CUISINE DESCRIPTION'] == 'American ']
    df_res_name = grade_count_overtime(df_res_name) 
    df_res_name['SUM'] = [float(df_res_name.iloc[i]['A'] + df_res_name.iloc[i]['B']*0 - df_res_name.iloc[i]['C'])/(df_res_name.iloc[i].sum()) for i in xrange(0, len(df_res_name.index))]
    df_sum = pd.DataFrame(df_res_name['SUM'])

    for res_name in type_name[1:]:
        df_res_name = df[df['CUISINE DESCRIPTION'] == res_name]
        df_res_name = grade_count_overtime(df_res_name) #grade count for each restaurant types in the top 10 type
        #calculate the score for each restaurant type
        #Score = (ratio of A)*1 + (ratio of B)*0 + (ratio of C)*(-1) 
        df_res_name[res_name] = [float(df_res_name.iloc[i]['A'] + df_res_name.iloc[i]['B']*0 - df_res_name.iloc[i]['C'])/(df_res_name.iloc[i].sum()) for i in xrange(0, len(df_res_name.index))]
        df_sum_current = pd.DataFrame(df_res_name[res_name])
        df_sum = pd.merge(df_sum, df_sum_current, left_index = True, right_index = True, how='outer') #merge dataframe for each restaurant type to one dataframe
    
    df_sum = df_sum.fillna(method='pad') #fill the missing data with previous value (since the dataset is sorted by date)
    df_sum = df_sum.dropna() #drop missing value after filling
    df_sum = df_sum.drop(df_sum.index[:200]) #drop the first 200 item, since at the very beginning, the amount of restaurant being inspected was very small, which cannot reflect the population
    df_sum.columns = ['American','Chinese','Coffee/Tea','Pizza','Italian','Latin','Japanese','Mexican','Bakery','Caribbean']
    return df_sum

#This function is to plot score overtime for each restaurant type in NYC
def top_10_plot(df):
    fig = plt.figure()
    df.plot(figsize=(10,8), linewidth = 1.5, color = ['dodgerblue','g','crimson','darkviolet','Tan','pink','orange','slategrey','aqua','lime']).legend(prop={'size':12}, ncol=2, loc='lower right')
    plt.title('Grade score overtime for top 10 types of restaurants in NYC')
    plt.savefig('results/Top_10_grade_score_overtime.png')
    plt.close(fig)

#This function is to plot correlation between any two restaurant types in NYC in color map
def top_10_colormap(df):
    corrmat = df.corr()
    fig = plt.figure()
    plt.pcolor(-corrmat, cmap = plt.cm.Greens)
    plt.xticks(np.arange(len(corrmat))+0.5, list(corrmat.columns), rotation=-25)
    plt.yticks(np.arange(len(corrmat))+0.5, list(corrmat.columns))
    plt.title('Correlation between top 10 types of restaurants in NYC')
    plt.savefig('results/top_10_corr.png')

def main():
    
    #load data
    df = load_data('../../assignment10_data/restaurants.csv', ['CAMIS','BORO','GRADE','GRADE DATE'])
    df = clean_data(df) #clean data
    
    #question 4
    sum_nyc, sum_boro = grade_sum(df) #calculate sum of test_grade in nyc and in each borough
    print 'The sum of test_grade in NYC is: {} \n'.format(sum_nyc)
    print 'The sum of test_grade in each boroughs is: \n {}'.format(sum_boro)
    
    #question 5
    grade_overtime_plot(df, 'nyc') #grade overtime plot for nyc
    #grade overtime plot for each borough
    for borough in ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']:
        df_boro = df[df['BORO'] == borough]
        grade_overtime_plot(df_boro, borough.lower())
    
    #question 6
    df1 = load_data('../../assignment10_data/restaurants.csv', ['CAMIS','CUISINE DESCRIPTION'])
    type_name = get_top_10_nyc(df1)
    df2 = load_data('../../assignment10_data/restaurants.csv', ['CAMIS','CUISINE DESCRIPTION', 'GRADE', 'GRADE DATE'])
    df2 = clean_data(df2)
    df2 = df2[df2['CUISINE DESCRIPTION'].isin(type_name)]
    df_sum = top_10_grade_overtime(df2, type_name) #calculate score overtime for each restaurant type
    top_10_plot(df_sum) #score overtime plot
    top_10_colormap(df_sum) #plot correlation between any two restaurant types in NYC in color map


if __name__ == '__main__':
    main()





