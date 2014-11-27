__author__ = 'leilu'
import pandas as pd
import matplotlib.pyplot as plt

def clean_data(df):
    col_to_keep = ['GRADE', 'CAMIS', 'DBA','BORO','GRADE DATE','CUISINE DESCRIPTION']
    df = df[col_to_keep]
    df = df[pd.notnull(df['GRADE'])]  # drop missing value
    grade_to_keep = ['A', 'B', 'C']  # only keep value that equals to 'A', 'B' or 'C'
    df = df[(df['GRADE']).isin(grade_to_keep)]  # drop value 'Z','P' and 'Not Yet Graded'
    return df

def test_grades(grade_list):
    """
    This function will take a list of string
    """
    trend = []
    for i in range(len(grade_list)-1):
        if grade_list[i] > grade_list[i+1]:
            trend.append(1)
        elif grade_list[i] < grade_list[i+1]:
            trend.append(-1)
        else:
            trend.append(0)
    if sum(trend) > 0:
        return 1
    elif sum(trend) < 0:
        return -1
    else:
        return 0


def test_restaurant_grades(data, camis_id):
    """ Check if the specified restaurant has an improving trend """
    grade_list = list(data[data['CAMIS'] == int(camis_id)].sort('GRADE DATE')['GRADE'])
    return test_grades(grade_list)

def graph(data, boro):
    """
    This function will plot a graph for the number of the restaurants with each grade at overtime given a borough
    :param data:  cleaned data
    :param boro: a borough such as queens
    :return: a plot
    """
    if boro == 'NYC':
        observation = data[:]
    else:
        observation = data[data['BORO'] == boro]

    for grade in ['A', 'B', 'C']:
        observation[observation['GRADE'] == grade].groupby('GRADE DATE')['GRADE'].count().plot(label=grade)

    plt.title('The number of restaurants in %s with each grade' %boro)
    plt.legend()
    plt.savefig('grade_improvment_%s' %boro.lower())
    plt.clf()  # clear the graph each time

def explore_data(data):
    """
    This function will explore more information about this data set
    :param data: data
    :return: summary statistics
    """

    col_to_keep = ['CUISINE DESCRIPTION','CAMIS', 'GRADE']
    data_6 = data[col_to_keep]
    by_grade_cuisine = data_6.groupby('CUISINE DESCRIPTION')
    print by_grade_cuisine['GRADE'].describe()


