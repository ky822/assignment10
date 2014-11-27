import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import functions 

#load dataframe
df = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
#remove the rows that have invalid grades or other invalid features
df = df.dropna()
df = df[df['GRADE'] != 'Not Yet Graded']
df = df.drop_duplicates()

def main():  
    grades_dict = {}
    camis_list = list(df.CAMIS.drop_duplicates())
    for camis in camis_list:
        grades_dict[camis] = functions.test_restaurant_grades(camis)
        
    city_grade = np.sum(grades_dict.values)
    print 'The sum of grade in NYC is: ' + str(city_grade)
    
    for boro in ['BRONX', 'QUEENS', 'BROOKLYN', 'MANHATTAN', 'STATEN ISLAND']:
        boro_camis_list = list(df[df.BORO == boro].CAMIS.drop_duplicates())
        boro_grade = 0
        for boro_camis in boro_camis_list:
            boro_grade += functions.test_restaurant_grades(boro_camis)
        print 'The sum of grades in ' + boro + ' is: ' + str(boro_grade)

    grade_over_time(df, 'nyc')
    q5b()    
    return

def grade_over_time(df, name):
    df_to_plot = df[['CAMIS', 'GRADE DATE', 'GRADE']]
    by_date = df_to_plot.groupby(['GRADE DATE', 'GRADE']).size()
    by_date = by_date.unstack().fillna(0)
    by_date.index = pd.to_datetime(by_date.index)
    by_date = by_date.sort_index()
    
    plt.figure(figsize = (10, 8))
    plt.plot(by_date.index, by_date['A'], 'r-', label = 'A')
    plt.plot(by_date.index, by_date['B'], 'c-', label = 'B')
    plt.plot(by_date.index, by_date['C'], 'p-', label = 'C')
    
    plt.legend(loc = 'best')
    plt.title('Number of restaurants in ' + name + ' for each grade over time')
    plt.xlabel('Time')
    plt.ylabel('Number of restaurants')
    plt.savefig('grade_improvement_' + name + '.pdf')
    
def q5b():
    for boro in ['BRONX', 'QUEENS', 'BROOKLYN', 'MANHATTAN', 'STATEN ISLAND']:
        boro_df = df[df.BORO == boro]
        grade_over_time(boro_df, boro)
    
if __name__ == '__main__':
    main()
