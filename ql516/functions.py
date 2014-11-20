# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 00:44:10 2014

@author: LaiQX
"""

import pandas as pd
import matplotlib.pyplot as plt


def data_clean(data_frame):
    cleaned_df = data_frame.dropna(how='any')
    cleaned_df = cleaned_df.loc[~(cleaned_df.GRADE == 'Not Yet Graded')]
    cleaned_df = cleaned_df.loc[~(cleaned_df.GRADE == 'P')]
    cleaned_df = cleaned_df.loc[~(cleaned_df.GRADE == 'Z')]
    cleaned_df = cleaned_df.loc[~(cleaned_df.BORO == 'Missing')]
    return cleaned_df


def test_grades(grade_list):
    n = len(grade_list)
    alphabet = dict(zip(['A', 'B', 'C'], [3,  2, 1]))
    equal = 0
    for i in range(n-1):
        if alphabet[grade_list[i]] < alphabet[grade_list[i+1]]:
            return -1
        if alphabet[grade_list[i]] == alphabet[grade_list[i+1]]:
            equal += 1
    if equal == n-1:
        return 0
    return 1    


def test_restaurant_grades(df, camis_id):
    data = df[['CAMIS', 'GRADE']]
    grade_list = list(data.loc[data.CAMIS == camis_id]['GRADE'])
    grade_is_improved = test_grades(grade_list)
    return grade_is_improved
 

def grade_test_count(df):
    data_used = df[['CAMIS', 'GRADE', 'BORO']]
    grouped_grade = data_used.groupby('CAMIS')
    improve_test = {}
    for name, groups in grouped_grade:
        temp = test_grades(list(groups['GRADE']))
        improve_test[name] = (temp, list(groups['BORO'])[0])
    improve_test = pd.DataFrame(improve_test)
    improve_test = improve_test.T
    improve_test.columns = ['INPROVE', 'BORO']
    result = improve_test.groupby('BORO').INPROVE.sum()
    f = open('GradeTestForEachBoroughs.txt', 'a+')
    f.write(str(result))
    f.close()


def date_format(date_str_list):
    year_list = [int(x[-4:]) for x in date_str_list]
    month_list = [int(x[:2]) for x in date_str_list]
    day_list = [int(x[3:5]) for x in date_str_list]
    date = [pd.datetime(year_list[i], month_list[i], day_list[i]) for i in xrange(len(year_list))]
    return date


def grade_plot(df, title):
    data = df[['CAMIS', 'GRADE', 'GRADE DATE']]
    date_str = list(data.loc[:, 'GRADE DATE'])
    date_list = date_format(date_str)
    data['DATE'] = date_list
    date_group = data.groupby('DATE')
    date_df = pd.DataFrame(columns=['A', 'B', 'C'], index=date_group.groups.keys())
    rest_series = pd.Series(index=data.groupby('CAMIS').groups.keys())
    for date, grade_groups in date_group:
        rest_series.ix[list(grade_groups['CAMIS'])] = list(grade_groups['GRADE'])
        a = sum(rest_series == 'A')
        date_df.ix[date, 'A'] = a
        date_df.ix[date, 'B'] = sum(rest_series == 'B')
        date_df.ix[date, 'C'] = sum(rest_series == 'C')
        print ">",
    plt.figure(figsize=(8, 6))
    date_df.plot()
    plt.title('grade_improvement_%s'%(title))
    plt.xlabel('Date')
    plt.ylabel('grade score')
    plt.savefig('grade_improvement_%s.pdf'%(title))
