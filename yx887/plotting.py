import pandas as pd
import numpy as np
from copy import copy
import matplotlib.pyplot as plt

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
        idx = new_df.index[i]
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

def plot_pie(df, name):
    """ plot a pie chart showing composition of different restaurants """
    # Get restaurant count group by description in descending order
    ranking = df.groupby('DESCRIPTION').count().sort('CAMIS', ascending=False)
    n = ranking.sum()[0] - ranking.ix['Other'][0]
    # Get top 10 descriptions and their corresponding counts
    other = n - ranking[:10].sum()[0]
    labels = list(ranking.index[:10])
    try:
        labels.remove('Other')
    except ValueError:
        pass
    sizes = []
    for label in labels:
        sizes.append(ranking.ix[label][0])
    labels = [x.decode('utf8').encode('ascii', 'replace') for x in labels]
    labels.append('Other')
    sizes.append(other)
        
    cm = plt.get_cmap('gist_rainbow')
    colors = [cm(x) for x in np.arange(0, 1, 1./len(labels))]

    plt.figure()
    plt.pie(sizes, labels=labels, colors = colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('Percentage of Different Restaurants ({})'.format(name))
    plt.axis('equal')
    plt.savefig('rest_pie_{}.png'.format(name))
    return 1
