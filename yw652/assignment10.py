import pandas as pd
import numpy as np
from scipy.stats import *
from plotting import *

def dataCleaning():
    '''
    data cleaning, keeping the essential columns and eliminate the rest
    :return: cleaned data set
    '''

    df = pd.read_csv("NYC Restaurant.csv")
    df = df[['CAMIS','GRADE','CUISINE DESCRIPTION','BORO','GRADE DATE']]
    df = df[(df.GRADE == 'A') | (df.GRADE == 'B') | (df.GRADE == 'C')]
    return df

def test_grades(grade_list):
    '''
    Testing the improvement: Split the grade list in half, and compare the modes of 2 parts
    Since the date is in a descending order, then if the mode1>mode2, then quality improves;
    if mode1=mode2, then the quality has not changed; if mode1<mode2, then the quality
    becomes worse
    :param grade_list:
    :return:score
    '''
    grade_dict = {'A':1,'B':0,'C':-1}
    grade_list_Numeric = [grade_dict[grade] for grade in grade_list]

    if len(grade_list_Numeric) == 1:
        return 0

    grade_list_firstHalf = grade_list_Numeric[0:len(grade_list)/2]
    grade_list_secondHalf = grade_list_Numeric[len(grade_list)/2:]

    mode1 = int(mode(grade_list_firstHalf)[0])
    mode2 = int(mode(grade_list_secondHalf)[0])

    #assuming date ordered started from the most recent one

    if mode1 > mode2:
        return 1
    elif mode1 == mode2:
        return 0
    else:
        return -1


def test_restaurant_grades(camis_id,NYCrestaurant):
    '''
    Given the dataset and the id the restaurant, the programs tells whether the given restaurant improves or not
    :param camis_id:
    :param NYCrestaurant:
    :return:score
    '''
    restaurantGRADE = NYCrestaurant[NYCrestaurant.CAMIS == camis_id].GRADE
    gradeLIST = []
    for grade in restaurantGRADE:
        gradeLIST.append(grade)

    return test_grades(gradeLIST)

def main():

    #Cleaning the data set and eliminate all the rows with an invalid grade
    NYCrestaurant = dataCleaning()

    if True:

        #Calculate the sum for ALL restaurants in New York
        sum1 = 0
        for id in NYCrestaurant.CAMIS.unique():
            sum1 = sum1 + test_restaurant_grades(id, NYCrestaurant)
        print 'Restaurant in New York has total score of ' + str(sum1)
        gradeGraph(NYCrestaurant, "New York City")

        #Calculate the sum for each of the borough
        boro = ['BROOKLYN','MANHATTAN','BRONX','QUEENS','STATEN ISLAND']
        for borough in boro:
            sum2 = 0
            restaurant = NYCrestaurant[NYCrestaurant.BORO == borough]
            gradeGraph(restaurant, "")
            for id in restaurant.CAMIS.unique():
                sum2 = sum2 + test_restaurant_grades(id,restaurant)
            print 'Restaurant in ' + borough + ' has total score of ' + str(sum2)

    if False:
        #Plot the degree of variety of restaurants in each borough
        varietyGraph(NYCrestaurant)
    if False:
        #plot the most common types of cuisine in NYC
        typeGraph(NYCrestaurant)




if __name__ == "__main__":
    main()