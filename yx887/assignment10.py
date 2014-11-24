import pandas as pd
import numpy as np
import sys
from preprocessing import *
from plotting import *

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
