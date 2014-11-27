import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#question 1: this function cleans the dataset, and keeps only the useful columns
def cleanData():
    df = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
    dfCl = df[((df.GRADE == 'A') | (df.GRADE == 'B') | (df.GRADE == 'C')) & (df.BORO != 'Missing')]
    df1 = dfCl[['CAMIS','CUISINE DESCRIPTION', 'BORO', 'INSPECTION DATE', 'SCORE', 'GRADE', 'GRADE DATE']]
    return df1

'''
question 2: this function tests the tendency of grade change by linear
regression. I first turn the Letter grade into number, where the higher 
the grade, the lower the score number. since the date is sorted from 
nearest to farthest, the slope would be positive if the score is imporving.
'''
def test_grades(grade_list):
    score = []
    for grade in grade_list:
        num = ord(grade)
        score.append(num)
    score = np.array(score).reshape(len(score),1)
    x = np.arange(len(grade_list)).reshape(len(grade_list),1)
    clf = linear_model.LinearRegression()
    clf.fit(x, score)
    slope = clf.coef_
    if slope > 0:
        return 1
    elif slope == 0:
        return 0
    else:
        return -1

#question 4: this function tests the grade change of a certain restaurant
def test_restaurant_grades(camis_id):
    camis = df[df.CAMIS == camis_id]
    camisGrade = camis['GRADE']
    return test_grades(camisGrade)
#question 5:the following 2 functions count and plot the restaurant of each grade 
def scores():
    boros = df.BORO.unique()
    scores = {}
    for boro in boros:
        dfBoro = df[df.BORO == boro]
        score = 0
        print boro
        for camis in dfBoro.CAMIS.unique():
            i = test_restaurant_grades(camis)
            score = score + i
        scores[boro] = score
    scores['NYC'] = sum(scores.values())
    return scores

def plotPdf(place, df):        
    plt.figure()
    ind = np.arange(5)
        
    plt.bar(ind, df['A'], color = 'r', label = 'A')
    plt.bar(ind, df['B'], color = 'y', bottom = df['A'], label = 'B')
    plt.bar(ind, df['C'], color = 'g', bottom = df['A']+df['B'], label = 'C')
    plt.ylabel('Scores')
    plt.xticks(ind, ('2010', '2011', '2012', '2013', '2014'))
    plt.title('Total Restaurant Scores for ' + place)
    plt.legend(loc = 'upper left')
    plt.savefig('grade_improvement_' + place +'.pdf', format = 'pdf', dpi = 72)
    plt.close('all')
        
             
    

