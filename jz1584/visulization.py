import matplotlib.pyplot as plt
import pandas as pd
 
def grade_series(grade,dataframe):
    """function takes grade, and return the series of numbers of restaurant 
    with that grade over time
    """
    Grade=dataframe[dataframe.GRADE==grade]
    sort_date=Grade.sort_index(by=['GRADE DATE'])
    grade_series=sort_date['GRADE DATE'].value_counts() 
    grade_series.columns=['Grade_%s'%grade]#assign column name to the series
    return grade_series


def plotGradeTrend(dataframe,area):
    """function generates the graph that shows the total number of restaurants in 
    new york city for each grade over time by using series from each grades
    """
    gradeA=grade_series('A',dataframe)
    gradeB=grade_series('B',dataframe)
    gradeC=grade_series('C',dataframe)
    merge_df=pd.concat([gradeA,gradeB,gradeC],join='outer',axis=1)
    #combine all the series from each grade
    merge_df.columns=['gradeA','gradeB','gradeC']
    #name the corresponding columns
    plot=merge_df.plot(title='Grade trend in %s' %area)
    plot.set_ylabel("Total number of Restaurants")
    plot.set_xlabel("Date")
    plt.savefig('grade_improvement_%s.pdf'%area)
    plt.close
    
    
