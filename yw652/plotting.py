import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def gradeGraph(NYCrestaurant,name):
    '''
    Generate the grade graph for each year in each borough, in the form of stacked bar
    :param NYCrestaurant:
    :param name:
    :return:
    '''
    df = NYCrestaurant
    name1 = df.BORO.unique()[0]
    df = df[['CAMIS','GRADE DATE','GRADE']]
    df['GRADE DATE'] = pd.to_datetime(df['GRADE DATE'])

    #Get the year of grading for each restaurant
    df['YEAR'] = pd.DatetimeIndex(df['GRADE DATE']).year

    #Group the data by grade and year, get the number of restaurant in each grade for each year
    data = df.groupby(['GRADE','YEAR']).size().unstack()

    gradeA = data.ix['A']
    gradeB = data.ix['B']
    gradeC = data.ix['C']

    #Plot the stacked bar graph: Grade A at the bottom, Grade B in the middle and Grade C at the top
    plt.bar([0,1,2,3,4], gradeA, color = 'green', label = 'grade A')
    plt.bar([0,1,2,3,4], gradeB, color = 'gray', bottom = gradeA, label = 'grade B')
    plt.bar([0,1,2,3,4], gradeC, color = 'yellow', bottom = gradeB+gradeA, label = 'grade C')

    plt.xticks([0.5,1.5,2.5,3.5,4.5],['2010','2011','2012','2013','2014'], rotation = "horizontal")
    plt.ylabel("Number of restaurant")
    plt.xlabel("Year")
    plt.legend(loc = "lower right")
    plt.title("Number of restaurant in each grades")
    if name == "":
        plt.savefig("Grade_Improvement_" + name1 + '.pdf')
    else:
        plt.savefig("Grade_Improvement_NYC.pdf")
    plt.close('all')

def varietyGraph(NYCrestaurant):
    '''
    Plot the degree of variety of cuisine types in each of the borough
    :param NYCrestaurant:
    :return:
    '''
    df = NYCrestaurant

    #Eliminate the missing boro data
    df = df[df.BORO != 'Missing']

    variety = df.groupby(['CUISINE DESCRIPTION','BORO']).size().unstack()
    totalNumber = len(variety)
    variety = variety.fillna(0)
    listofVariety = {}

    #Construct a dictionary with key being the borough, and the values being the percentages of variety for each borough
    for borough in variety:
        boro = variety[borough]
        count = len(boro[boro != 0])
        listofVariety.update({borough:(float(count)/totalNumber)})

    #Plotting the bar graph
    plt.bar(range(len(listofVariety)), listofVariety.values(), align = 'center', width = 0.35)
    plt.xticks(range(len(listofVariety)), listofVariety.keys(), fontsize = 8)
    plt.ylabel("Percentage of variety")
    plt.xlabel("Boroughs of New York")

    plt.savefig("Variety bar graph for all boroughs.pdf")

def typeGraph(NYCrestaurant):
    '''
    Plotting the pie chart that indicates the top 20 most common type of cuisines in NYC
    :param NYCrestaurant:
    :return:
    '''
    df = NYCrestaurant

    #Get the counts for each cuisine types in NYC
    category = df.groupby(['CUISINE DESCRIPTION']).size()

    category.sort(axis = 1, ascending = False)
    dominant = category[:20]
    label = list(dominant.index)
    values = list(dominant.values)
    sizes = []
    for value in values:
        sizes.append(value/float(sum(values)))

    plt.pie(sizes,labels = label, autopct = '%1.1f%%', shadow = True, startangle=90)
    plt.axis('equal')

    plt.savefig("Rank of variety.pdf")








