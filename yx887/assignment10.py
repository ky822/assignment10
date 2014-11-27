import pandas as pd
import numpy as np
import sys
from preprocessing import *
from plotting import *
from grading import *

def main():
    # Question 2
    args = sys.argv[1:]
    try:
        df = pd.read_csv(args[0], low_memory=False)
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
