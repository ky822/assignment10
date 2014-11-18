import pandas as pd
import numpy as np
import sys
from copy import copy
import matplotlib.pyplot as plt

def house_keeping(df):
    """ Data cleaning """
    gradings = df[['CAMIS', 'BORO', 'GRADE', 'GRADE DATE']]    # only need 4 cols
    gradings = gradings[(gradings.GRADE=='A') | (gradings.GRADE=='B') | (gradings.GRADE=='C')]
    gradings = gradings.drop_duplicates()
    gradings['GRADE DATE'] = pd.to_datetime(gradings['GRADE DATE'])    # change data type to datetime
    return gradings

def grade_count_series(df):
    """ Take in a data frame and generate series of restaurant count in each grade and their corresponding date. """
    n = len(df)
    previous_grade = {}    # Store previous grade for each restaurant in a dictionary
    new_df = df.sort('GRADE DATE')
    current_date = new_df['GRADE DATE'].iloc[0]
    dates = [current_date]    # Store grade dates
    counts = []
    count = {'A': 0, 'B': 0, 'C': 0}
    # Loop through each grading record
    for i in xrange(n):
        row = new_df.iloc[i]
        # Update count if grade date changes
        if row['GRADE DATE'] != current_date:
            counts.append(copy(count))
            current_date = row['GRADE DATE']
            dates.append(current_date)
        idx = row['CAMIS']
        grade = row['GRADE']
        # Do something if we see the restaurant before
        if idx in previous_grade:
            if previous_grade[idx] == grade:    # Pass if the grade does not change
                pass
            else:    # Count for old grade minus 1, count for new grade plus 1
                count[grade] += 1
                count[previous_grade[idx]] -= 1
                previous_grade[idx] = grade
        # Record the restaurant in the dictionary if it's new
        else:
            previous_grade[idx] = grade
            count[grade] += 1
    counts.append(copy(count))    # Add last count
    return pd.DataFrame(counts), dates

def plot_grades(counts, dates, name):
    """ Plot time series data """
    plt.figure()
    plt.plot_date(dates, counts['A'], 'r-', label='A')
    plt.plot_date(dates, counts['B'], 'b-', label='B')
    plt.plot_date(dates, counts['C'], 'g-', label='C')
    plt.legend(loc='upper left')
    plt.title('Number of Restaurant in Each Grade ({})'.format(name.upper()))
    plt.ylabel('Count')
    plt.savefig('grade_improvement_{}.pdf'.format(name.split(' ')[0]))
    return 1
    
# Question 3
def test_grades(grade_list):
    """ test whether a list of grades has an increasing trend by fit a linear regression model to it """
    n = len(grade_list)
    if n == 1:
        return 0
    x = np.arange(0, 2, 2./n)
    A = np.array([x, np.ones(n)])
    grade_dict = {'A': 2, 'B': 1, 'C': 0}
    try:
        y = [grade_dict[g] for g in grade_list]
    except KeyError as e:
        sys.exit('There should only be 3 levels of grades: A, B, or C')        
    w = np.linalg.lstsq(A.T, y)[0]
    
    # We got the 0.375 magic number by assuming the sequence A, B, B, B, A, A, A has an increasing trend
    if w[0] > 0.375:
        trend = 1
    elif w[0] < -0.375:
        trend = -1
    else:
        trend = 0
    return trend

def test_restaurant_grades(df, camis_id):
    """ Check if the specified restaurant has an improving trend """
    # Get the list of grades sorted by date
    grade_list = list(df[df['CAMIS']==int(camis_id)].sort('GRADE DATE')['GRADE'])
    return test_grades(grade_list)

def main():
    # Question 2
    args = sys.argv[1:]
    try:
        df = pd.read_csv(args[0])
    except IndexError:
        sys.exit('Need to specify the data file.')
    print 'Cleaning data ...'
    gradings = house_keeping(df)

    # Question 4
    idxs = gradings['CAMIS'].unique()
    total = 0
    print 'Calculating trends ...'
    # Calculate value for the whole city
    for idx in idxs:
        total += test_restaurant_grades(gradings, idx)
    print 'Summation of the trending identifiers is:\nNYC: {}'.format(total)
    
    boroughs = gradings['BORO'].unique()
    sums = []
    # Calculate the value by borough
    for boro in boroughs[:-1]:    # Rule out missing boroughs
        df_boro = gradings[gradings['BORO']==boro]
        idxs_boro = df_boro['CAMIS'].unique()
        tot = 0
        for idx in idxs_boro:
            tot += test_restaurant_grades(df_boro, idx)
        sums.append(tot)
    for i in range(len(sums)):
        print '{0}: {1}'.format(boroughs[i], sums[i])

    # Question 5
    print 'Counting restaurants and plotting ...'
    counts, dates = grade_count_series(gradings)
    plot_grades(counts, dates, 'nyc')
    for boro in boroughs[:-1]:
        counts_boro, dates_boro = grade_count_series(gradings[gradings['BORO']==boro])
        plot_grades(counts_boro, dates_boro, boro.lower())
    
if __name__ == '__main__':
    main()    
