import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def cleanData():
    '''
    clean the data. Keep those data whose 'GRADE' label is A or B or C. And just keep four features. Then change the datetime.
    '''
    data = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')

    # just keep those data whose grade is 'A' or 'B' or 'C'.
    data = data[(data['GRADE'] == 'A') | (data['GRADE'] == 'B') | (data['GRADE'] == 'C')]

    # just keep those four features
    data = data[["CAMIS", "BORO", "GRADE", "GRADE DATE"]]
    data['GRADE DATE'] = pd.to_datetime(data['GRADE DATE'])

    return data


def test_grades(grade_list):
    '''
    The function returns 1 if the grades for the restaurant are improving, -1 if they are declining, or 0 if they have stayed the same.
    '''

    # Divide the grade list into two parts and calculate the scores of each parts. Let A be score 1 and B be score 0 and C be score -1. If the second part's scores minus the first part's scores are more than 1, we will return 1 and if less than -1, we'll return -1, otherwise, return 0.
    size = len(grade_list)
    firstHalfGrades = 0
    secondHalfGrades = 0

    # calculate the score of the first part
    for i in range(size / 2):
        if grade_list[i] == 'A':
            firstHalfGrades += 1
        elif grade_list[i] == 'B':
            firstHalfGrades += 0
        else:
            firstHalfGrades += -1

    # calculate the score of the second part.
    for i in range(size / 2 + 1, size):
        if grade_list[i] == 'A':
            secondHalfGrades += 1
        elif grade_list[i] == 'B':
            secondHalfGrades += 0
        else:
            secondHalfGrades += -1

    # judge the difference of the two parts' scores and return the result.
    if secondHalfGrades - firstHalfGrades > 1:
        return 1
    elif secondHalfGrades - firstHalfGrades < -1:
        return -1
    else:
        return 0


def test_restaurant_grades(df, camis_id):
    '''
    The function judges whether the resturant of the given camis_id has improved over the date.
    '''
    grade = list(df.GRADE[df.index == int(camis_id)])

    # for the date is in reverse order, so we need to return minus test_grades(grade)
    return -test_grades(grade)


def plotTotalGrades():
    df = cleanData()
    df = df.dropna()
    plt.figure()
    df_grade_A = df[df['GRADE'] == 'A']
    df_grade_A.groupby(by='GRADE DATE')['GRADE'].count().plot()
    df_grade_B = df[df['GRADE'] == 'B']
    df_grade_B.groupby(by='GRADE DATE')['GRADE'].count().plot()
    df_grade_C = df[df['GRADE'] == 'C']
    df_grade_C.groupby(by='GRADE DATE')['GRADE'].count().plot()
    plt.xlabel('Date')
    plt.ylabel('Numbers')
    plt.title('Grade Improvement of NYC')
    plt.savefig("grade_improvement_nyc.pdf")


def plotEachBorough():
    borough = ['BRONX', 'BROOKLYN', 'QUEENS', 'MANHATTAN', 'STATEN ISLAND']
    for area in borough:
        df = cleanData()
        df = df.dropna()
        plt.figure()
        df2 = df[df['BORO'] == area]
        df_grade_A = df2[df2['GRADE'] == 'A']
        df_grade_A.groupby(by='GRADE DATE')['GRADE'].count().plot()
        df_grade_B = df2[df2['GRADE'] == 'B']
        df_grade_B.groupby(by='GRADE DATE')['GRADE'].count().plot()
        df_grade_C = df2[df2['GRADE'] == 'C']
        df_grade_C.groupby(by='GRADE DATE')['GRADE'].count().plot()
        plt.xlabel('Date')
        plt.ylabel('Numbers')
        if area != 'STATEN ISLAND':
            plt.title('Grade Improvement of {}'.format(area))
            plt.savefig("grade_improvement_{}.pdf".format(area))
        else:
            plt.title('Grade Improvement of STATEN')
            plt.savefig("grade_improvement_STATEN.pdf")


def showScore():
    '''
    showthe total scores of the inspection of each restaurant.
    '''
    score = []
    df = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
    df = df[["CAMIS", "SCORE"]]
    df = df.set_index('CAMIS')
    df = df.dropna()
    uniqueIndex = df.index.unique()
    for idx in uniqueIndex:
        score.append(sum(df.SCORE[df.index == int(idx)]))
    plt.figure()
    plt.plot(range(len(score)), score)
    plt.xlabel('Each restaurant')
    plt.ylabel('Total Scores of inspection of each restaurant')
    plt.savefig('Total scores of inspection of each resturants.png')
