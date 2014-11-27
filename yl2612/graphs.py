import pandas as pd
import matplotlib.pyplot as plt

def grade_graph(df,area):
    '''
    Generate a graph that shows the total number of restaurants for each grade over time.
    '''
    count_grades = df.apply(pd.Series.value_counts, axis=1) #count the number of grades at different dates
    uncapitalized_area = area.lower()
    plt.figure()
    count_grades.plot()
    plt.title('grade improvement in {}'.format(uncapitalized_area))
    plt.savefig('grade_improvement_{}.pdf'.format(uncapitalized_area.split(' ')[0]))
    
   
def bar_grade(df):
    '''
    Create a bar plot for q6 that shows the number of restaurants in different cuisines.
    '''
    plt.figure(figsize=(10, 8))
    df.plot(y='Count', kind='bar',rot=45,fontsize=9)#create a bar plot
    plt.title('Number of restaurants in different cuisines')
    plt.savefig('Number_of_restaurants_in_different_cuisines.pdf')
