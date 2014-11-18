import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def gradeplot(df, name):
    """plot the grade"""
    data = df[:]
    data = data[['CAMIS', 'GRADE DATE', 'GRADE']]
    by_date_grade = data.groupby(['GRADE DATE', 'GRADE'])
    data_date_grade = by_date_grade.size().unstack().fillna(0)
    data_date_grade.index = pd.to_datetime(data_date_grade.index)  # change format to datetime
    data_date_grade = data_date_grade.sort_index()
    data_date_grade = data_date_grade[['A', 'B', 'C']]
    plt.figure()
    plt.plot(data_date_grade.index, data_date_grade['A'], 'r-', label = 'A')
    plt.plot(data_date_grade.index, data_date_grade['B'], 'g-', label = 'B')
    plt.plot(data_date_grade.index, data_date_grade['C'], 'b-', label = 'C')
    plt.legend(loc=2)
    plt.title("Number of restaurants in NYC for each grade")
    plt.ylabel("# of restaurants")
    plt.savefig('grade_improvement_' + name + '.pdf')


def test_grades(grade_list):
    """This function splits grade_list to first half and second half and uses difference of median grade in each split
    as a indicator.
    If median score of first half is higher than the score of second half, it will return 1
    If median score of first half is lower than the score of second half, it will return -1
    If median score of first half equals the score of second half, it will return 0
    If there is only one score, it will return 0
    """
    data = pd.Series(grade_list[:])
    clean_data = data[(data == 'A') | (data == 'B') | (data == 'C')]  # drop letters
    if len(clean_data) == 1:
        return 0
    ord_list = map(ord, clean_data)
    first_half = ord_list[:int(0.5*len(ord_list))]
    second_half = ord_list[int(0.5*len(ord_list)):]
    if np.median(first_half) < np.median(second_half):
        return 1
    elif np.median(first_half) > np.median(second_half):
        return -1
    else:
        return 0


def import_clean_data(document):
    df = pd.read_csv(document)
    cleaned = df[:]
    isnul = (df['GRADE'].isnull() == False)
    index = isnul[isnul].index
    cleaned = cleaned.ix[index]
    cleaned = cleaned.drop_duplicates(subset=['CAMIS', 'GRADE DATE', 'GRADE'])
    cleaned.index = cleaned['CAMIS']
    return cleaned
