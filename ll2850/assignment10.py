__author__ = 'leilu'

import numpy as np
import pandas as pd
from package.supporting_functions import *

data = pd.read_csv('restaurant_data.csv', header=0, sep=',', low_memory=False)
df = pd.DataFrame(data)


def main():
    try:

        # Question 4
        clean_df = clean_data(df)
        camis_id = clean_df['CAMIS'].unique()

        total_grade = []
        for id in camis_id:
            grade = test_restaurant_grades(clean_df, id)
            total_grade.append(grade)
        print "The total grade for all restaurants in the city is :" + str(sum(total_grade))

        if sum(total_grade) < 0:
            print "The overall rating trend in the city is declining"
        elif sum(total_grade) > 0:
            print "The overall rating trend in the city is improving"
        else:
            print "The overall rating trend in the city is constant"

        boro_list = clean_df['BORO'].unique()[:-1]

        for boro in boro_list:
            boro_data = clean_df[clean_df['BORO'] == boro]
            boro_restaurant_id = boro_data['CAMIS'].unique()
            total_boro = []
            for i in boro_restaurant_id:
                grade_boro = test_restaurant_grades(boro_data, i)
                total_boro.append(grade_boro)
            print "the total grade for %s is %d." % (boro,  sum(total_boro))
            if sum(total_boro) < 0:
                print "The overall rating trend in %s is declining." %boro
            elif sum(total_boro) > 0:
                print "The overall rating trend in %s is improving." %boro
            else:
                print "The overall rating trend in %s is constant." %boro

        # Question 5
        borough = boro_list.tolist()
        borough.append('NYC')
        for boro in borough:
            graph(clean_df, boro)

        # Question 6
        explore_data(clean_df)
        #This data set is useful for assessing the quality of shops in the city
    except(KeyboardInterrupt, EOFError):
        print "Oops!"


if __name__ == '__main__':
    main()