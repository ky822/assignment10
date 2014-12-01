'''
Created on Nov 29, 2014

@author: keye
'''
import pandas as pd
import matplotlib.pyplot as plt

def GenerateGraph(df,area):
    """
    Generate a grade_improvement graph for Questions 5 
    """
    plt.figure()
    df[df.GRADE=='A'].groupby(by='GRADE DATE').GRADE.count().plot()
    df[df.GRADE=='B'].groupby(by='GRADE DATE').GRADE.count().plot()
    df[df.GRADE=='C'].groupby(by='GRADE DATE').GRADE.count().plot()
    plt.xlabel('GRADE_DATE')
    plt.ylabel('Number_of_Restaurants')
    plt.title('grade_improvement_{}'.format(area))
    plt.savefig("grade_improvement_{}.pdf".format(area))
    print '\nGraph grade_improvement_{} has been created!'.format(area)

def GenerateGraph_Question6(df):
    """
    Generate a pie to show the percentages of the top 10 cuisines for NYC restaurants.
    """
    
    size = pd.value_counts(df['CUISINE DESCRIPTION'].ravel())
    label_list = df['CUISINE DESCRIPTION'].unique()
    label = []
    #Set the parameter for plotting.
    for i in range(10):
        label.append(label_list[i])
    label[2]='Tea and Coffee'
    labels = label[0],label[1],label[2],label[3],label[4],label[5],label[6],label[7],label[8],label[9]
    sizes = size[0],size[1],size[2],size[3],size[4],size[5],size[6],size[7],size[8],size[9]
    explode = (0.15,0.13,0.12,0,0,0,0,0,0,0)
    colors = ['b','lightskyblue','c','purple','m','g','yellowgreen','lightgreen','gold','lightcoral']
    #Plot a pie.
    plt.figure()
    plt.pie(sizes, explode=explode, autopct='%1.1f%%',colors=colors,labels=labels)
    plt.axis('equal')
    plt.title('Percentage of the top 10 cuisines')
    plt.savefig('Pie of Cuisines')
    print '\nA Pie of Cuisines is created!'