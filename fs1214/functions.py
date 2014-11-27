'''
Created on 2014.11.23

@author: apple
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.cm as cm


"""
Load the csv data into a dataframe, and clean up the data as following.
1.We only need 'CAMIS', 'BORO', 'GRADE', 'GRADE DATE' these four columns, let result_df be our return dataframe.
2.Only when 'GRADE' is 'A','B',or 'C', it is valid.
3.Drop the duplicates of this dataframe.
4.Make 'GRADE DATE' to the datatime type.
5.Let 'CAMIS' to the index
6.Sort by 'GRADE DATE'
"""
def cleandata(filename):
    df = pd.read_csv(filename)
    result_df = df[['CAMIS', 'BORO', 'GRADE', 'GRADE DATE']]
    grademask = (result_df.GRADE=='A') | (result_df.GRADE=='B') | (result_df.GRADE=='C')
    result_df = result_df[grademask]
    result_df = result_df.drop_duplicates(subset=['CAMIS','BORO','GRADE DATE','GRADE'])
    result_df['GRADE DATE'] = pd.to_datetime(result_df['GRADE DATE'])
    result_df = result_df.set_index(keys='CAMIS')
    result_df = result_df.sort('GRADE DATE')
    return result_df

"""
Clean the data for question 6
"""
def cleandata_6(filename):
    #clean the data
    df = pd.read_csv(filename)   
    newdf = df[['CAMIS', 'CUISINE DESCRIPTION','GRADE','GRADE DATE']]
    newdf = newdf.drop_duplicates(subset=['CAMIS', 'CUISINE DESCRIPTION','GRADE','GRADE DATE']) 
    grademask = (newdf.GRADE=='A') | (newdf.GRADE=='B') | (newdf.GRADE=='C')
    newdf = newdf[grademask]
    newdf['GRADE DATE'] = pd.to_datetime(newdf['GRADE DATE'])
    newdf = newdf.dropna()
    newdf = newdf.set_index(keys='CAMIS')
    newdf = newdf.sort('GRADE DATE')
    return newdf
"""
A list of grades, as the input, has been sorted by date. 
Returns 1 if the grades are improving, -1 if they are declining, or 0 if they have stayed the same.
In this case, I use scipy.stats.linregress to fit the grades into a linear model. 
If the slope of the model is more than 0.3, we assume the grades are increasing;
if the slope of the model is less than -0.3, we assume the grades are decreasing;
if the slope of the model is between -0.3 and 0.3, we assume the grades are the same.
"""
def test_grades(grade_list):
    length = len(grade_list)
    #If grade_list only contain one grade, we assume the grade stays the same.
    if length == 1:
        return 0
    x = np.arange(length)
    #Transfer the grade into the values, let 'A':2,'B':1,'C':0.
    grade_dict = {'A':2,'B':1,'C':0}
    y = np.array([grade_dict[g] for g in grade_list])
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    if slope > 0.2:
        return 1
    elif slope < -0.2:
        return -1
    else:
        return 0

"""
Using test_grades(grade_list), we only need to get a list of every restaurant's grades.
We should sort the data by 'GRADE DATE'.
"""
def test_restaurant_grades(df,camis_id):
    restaurant_grade = df.loc[camis_id,['GRADE','GRADE DATE']]
    grade_list = list(restaurant_grade.GRADE)
    test = test_grades(grade_list)
    return test

"""
For every date, we should count the numbers of restaurants for each grade. 
More importantly, every restaurant should have one or several grades over time. 
Between the two dates, we assume that the grade for this restaurant stays the same as the former one.

Returns:
        counts: {'A':[],'B':[],'C':[]}.
        date_list: []
        counts['A'], counts['B'], or counts['C'] and date_list are correspondingly matched. 
"""
def grade_counts(df):
    
    #We already sort the dataframe by 'GRADE DATE' in function cleandata. Set the initial date of latest_date.
    latest_date= df['GRADE DATE'].iloc[0]
    #Save the values of dates into a list named date_list
    date_list = [latest_date]       
    
    #Save the total numbers of restaurants for each grade over time into a dictionary 'counts'.
    counts = {'A':[],'B':[],'C':[]}
    #A dictionary 'count_dict' stores the numbers of restaurants for each grade in one specific date.
    count_dict = {'A': 0, 'B': 0, 'C': 0}
    #A dictionary 'former_grade' stores the grades of restaurants.
    former_grade = {}
    
    for i in range(len(df)):
        #Get every row in dataframe
        row = df.iloc[i]
        
        if row['GRADE DATE'] != latest_date:
            #Update the latest date and append it into date_list.
            latest_date= row['GRADE DATE']
            date_list.append(latest_date)
            #Save the results of counts into the dictionary 'counts'.
            counts['A'].append(count_dict['A'])
            counts['B'].append(count_dict['B'])
            counts['C'].append(count_dict['C'])
        
        #index actually is the value of 'CAMIS'.
        index = df.index[i]
        grade = row['GRADE']
        if index in former_grade:
            #If former_grade has saved this restaurant's grade, delete it.
            count_dict[former_grade[index]] = count_dict[former_grade[index]] - 1
        
        #Save the restaurant's grade again.
        former_grade[index] = grade
        count_dict[grade] = count_dict[grade] + 1
    
    #Save the last results.
    counts['A'].append(count_dict['A'])
    counts['B'].append(count_dict['B'])
    counts['C'].append(count_dict['C'])
    return counts, date_list


"""
Plot the graph of question5. Use the return of function grade_counts.
Question5 a: the input district should be 'nyc'.
Question5 b: the input district should be each borough.
"""
def grade_plot(df,district):
    
    y, x = grade_counts(df)
    plt.figure()
    plt.plot(x,y['A'],'r',label = 'Grade: A')
    plt.plot(x,y['B'],'b',label = 'Grade: B')
    plt.plot(x,y['C'],'g',label = 'Grade: C')
    plt.legend(loc = 2)
    plt.xlabel('Grade Date')
    plt.ylabel('The Number of Restaurants')
    plt.title('The Total Number of Restaurants in {} for Each Grade'.format(district))
    plt.savefig('grade_improvement_{}.pdf'.format(district))

"""
Plot the pie chart for question 6.
"""
def pie_plot(newdf):
                                          
    #Get the size of groups by 'CUISINE DESCRIPTION'.
    groupsize = newdf.groupby('CUISINE DESCRIPTION').size()
    groupsize.sort() 
    
    #total_number is the number of all the restaurants. We only show the top 12 restaurants.
    total_number = len(newdf)
    #We get the percentage of top 10 restaurants, adding the restaurants out of 10 to 'Others'.
    top_10 = groupsize[-10:]/total_number
    top_10['Other'] = float(groupsize[:-10].sum())/total_number
    
    #Clean the list. 
    #Let 'Cafe/Coffee/Tea' substitute 'Caf?/Coffee/Tea','Latin (Cuban etc.)' substitute Latin (Cuban, Dominican, Puerto Rican, South & Central American).
    top_10_list = list(top_10.index)
    top_10_list[4] = 'Cafe/Coffee/Tea'
    top_10_list[5] = 'Latin (Cuban etc.)'
    
    #Plot the pie chart.
    plt.figure(figsize=(8,8))
    plt.pie(top_10,labels = top_10_list,autopct='%1.1f%%',colors=cm.rainbow(np.linspace(0,1,11)))
    plt.title('The Top 10 Cuisine in NYC')
    plt.savefig('piechart_top10_nyc.png')

"""
In every kind of top 10 restaurant, we compute the grade sum of them, 
and figure out the total condition of these types of restaurants over time.
"""
def grade_cuisine_plot(df):
    #Get the size of groups by 'CUISINE DESCRIPTION'.
    groupsize = df.groupby('CUISINE DESCRIPTION').size()
    groupsize.sort() 
    
    #Get the top 10 list
    top_10 = groupsize[-10:]
    top_10_list = list(top_10.index)
    top_10_name = top_10_list[:]
    top_10_name[4] = 'Cafe/Coffee/Tea'
    top_10_name[5] = 'Latin (Cuban etc.)'
    
    plt.figure()
    colors=cm.rainbow(np.linspace(0,1,10))
    
    i = 0
    for it in top_10_list:
        grade_cuisine = df[df['CUISINE DESCRIPTION']==it]
        #Get the numbers of restaurants in each grade over time
        counts, date_list = grade_counts(grade_cuisine)       
        #We assume that A represents 2 points, B represents 1 point, C represents 0.
        counts['sum'] = (np.array(counts['A'])*2 + np.array(counts['B'])*1 +np.array(counts['C'])*0)
        plt.plot(date_list,counts['sum'],color=colors[i],label = top_10_name[i])
        i = i+1
    plt.legend(loc=2)
    plt.xlabel('Date Time')
    plt.ylabel('the sum of grade of restaurants')
    plt.title('The Sum of Grade of Top 10 Cuisine over time in NYC')
    plt.savefig('grade_cuisine_plot.png')