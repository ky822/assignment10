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
    return gradings.set_index('CAMIS')

def house_keeping_v2(df):
    """ Data cleaning for question 6 """
    new_df = df[['CAMIS', 'BORO', 'CUISINE DESCRIPTION']]
    new_df = new_df.drop_duplicates()
    new_df.columns = ['CAMIS', 'BORO', 'DESCRIPTION']
    return new_df

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
    
# Question 3
def test_grades(grade_list, reverse=False):
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
    return -trend if reverse else trend

def test_restaurant_grades(df, camis_id):
    """ Check if the specified restaurant has an improving trend """
    # Get the list of grades sorted by date
    grade_list = list(df.GRADE[df.index==int(camis_id)])
    return test_grades(grade_list, reverse=True)

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
    idxs = gradings.index.unique()
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
        idxs_boro = df_boro.index.unique()
        tot = 0
        for idx in idxs_boro:
            tot += test_restaurant_grades(df_boro, idx)
        sums.append(tot)
    for i in range(len(sums)):
        print '{0}: {1}'.format(boroughs[i], sums[i])

    # Question 5: There is a general improvement of restaurants going on in the city
    print 'Counting restaurants and plotting ...'
    counts, dates = grade_count_series(gradings)
    plot_grades(counts, dates, 'nyc')
    for boro in boroughs[:-1]:
        counts_boro, dates_boro = grade_count_series(gradings[gradings['BORO']==boro])
        plot_grades(counts_boro, dates_boro, boro.lower())

    # Question 6: We can find out the percentages of American food, Chinese food, Italian food, etc in the whole city and in each borough
    print 'Cooking pie ...'
    new_df = house_keeping_v2(df)
    plot_pie(new_df, 'nyc')    # Only nyc data is used here for demostration
    
if __name__ == '__main__':
    main()    
