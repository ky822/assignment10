s__author__ = 'chianti'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''
PreprocessingData() is used to read and clean the data set.
It returns a DataFrame with sorted 'DRADE DATE' column.
'''
def PreprocessingData():
    
    # Load the CSV file into a DataFrame
    raw_data = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')

    
    # In this certain problem, only four columns are useful. So let's delete the rest of the columns.
    selected_data = raw_data[['CAMIS', 'BORO', 'GRADE', 'GRADE DATE']]
    
    # Drop the rows which are duplicate in the DataFrame
    raw_data = raw_data.drop_duplicates()    
    
    # Delete the rows with invalid GRADE values or invalid BORO values
    new_data = selected_data[(selected_data.GRADE == 'A') | (selected_data.GRADE == 'B') | (selected_data.GRADE == 'C')]
    new_data = new_data[new_data.BORO != 'Missing']
    
    # Convert the 'GRADE DATE' values to pandas datetime type
    new_data['GRADE DATE'] = pd.to_datetime(new_data['GRADE DATE'])
    
    return new_data


'''
test_grades(grade_list) takes a list of grades sorted in date order,
and returns 1 if the grades are improving, -1 if they are declining, or 0 if they have stayed the same.
For example:
           test_grades(['A', 'B', 'C', 'B', 'C']) will return -1
           test_grades(['C', 'B', 'C', 'A', 'A']) will return 1
To do that, first change the alphabet letters to numbers using ord(), then compute the mean of the first half of the
numbers and the mean of the rest of the numbers. If they are the same, return 0. If the first one is bigger, return 1.
Else, return -1. Moreover, this function considers the situation that there is just one grade in the grade_list, and it
returns 0 in this case.
'''
def test_grades(grade_list):

    # Use ord() to convert alphabet letters to numbers, so that A is 65, B is 66, C is 67 now.
    numbers = [ord(each_letter) for each_letter in grade_list]

    # Compute the mean of the first half of the numbers and the mean of the rest
    beginning_score = np.mean(numbers[: int(len(grade_list)*.5)+1])
    ending_score = np.mean(numbers[int(len(grade_list)*.5)+1:])

    if len(grade_list) == 1:
        return 0
    elif beginning_score == ending_score:
        return 0
    elif beginning_score > ending_score:
        return 1
    else:
        return -1

'''
Given a CAMIS ID (type: int), test_restaurant_grades(camis_id) returns 1 if the grades for the restaurant are improving,
-1 if they are declining, or 0 if they have stayed the same.
'''
def test_restaurant_grades(camis_id):

    # Read and clean the data set
    data = df

    # select the rows of data set whose CAMIS values match the camis_id value
    one_restaurant_data = data[data.CAMIS == camis_id]

    # Sort one_restaurant_data by 'GRADE DATE'
    sorted_one_restaurant_data = one_restaurant_data.sort(columns='GRADE DATE', ascending=True)

    # Get the list of GRADE values which are sorted in data order
    grades = sorted_one_restaurant_data['GRADE']
    grade_list = list(grades)

    # Use test_grades(grade_list) to examine whether the grades are improving over time
    improving_grades = test_grades(grade_list)

    return improving_grades


'''
This function is used to reconstruct data_frame.
It returns a DataFrame with index set to be sorted dates
It also represents the number of A, B, C grades for each date.
'''
def Reconstruct_to_plot(data_frame):
    grades_overtime = data_frame.groupby(['GRADE DATE', 'GRADE']).size()
    grades_overtime = grades_overtime.unstack().fillna(0)
    grades_overtime = grades_overtime.sort_index()
    return grades_overtime


'''
Plot_Grades_Over_Time(data_frame) generates a graph that shows the total number of restaurants in NYC for each grade
over time
'''
def Plot_Grades_Over_Time(data_frame, name):

    # First, reconstruct the data_frame so that it will be easy to plot
    grades_overtime = Reconstruct_to_plot(data_frame)

    # Next, generate the figure
    plt.figure()

    plt.plot(grades_overtime.index, grades_overtime['A'], 'r-', label='A')
    plt.plot(grades_overtime.index, grades_overtime['B'], 'c-', label='B')
    plt.plot(grades_overtime.index, grades_overtime['C'], 'b-', label='C')
    plt.title(name.upper())

    plt.legend(loc='best')
    plt.xlabel('Date')
    plt.xticks(rotation=30)

    plt.ylabel('Num of restaurants')

    plt.savefig('grade_improvement_' + name.lower().split(' ')[0] + '.pdf')

    plt.show()

df=PreprocessingData()

# Note: The above functions are used for Question 1-5
#       The following functions are used for Question 6

'''
This function uses the data set to generate a DataFrame with valid CUISINE DESCRIPTION, SCORE, INSPECTION DATE values.
Besides, INSPECTION DATE is set to be the index.
The CUISINE DESCRIPTION values can only be Korean, Indian, Chinese, Mexican, Italian, or Thai.
'''
def PreprocessingCuisineData():

    # Load the CSV file into a DataFrame
    raw_data = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')

    # In this certain problem, only four columns are useful. So let's delete the rest of the columns.
    selected_data = raw_data[['CUISINE DESCRIPTION', 'SCORE', 'INSPECTION DATE']]

    # Drop the rows which are duplicate in the DataFrame
    selected_data = selected_data.drop_duplicates()

    # Delete the rows with invalid SCORE values.
    new_data = selected_data[selected_data.SCORE.isnull() == False]

    # Delete the rows with cuisine types I'm not interested in
    new_data = new_data[(new_data['CUISINE DESCRIPTION'] == 'Korean') | (new_data['CUISINE DESCRIPTION'] == 'Indian') |
                        (new_data['CUISINE DESCRIPTION'] == 'Chinese') | (new_data['CUISINE DESCRIPTION'] == 'Mexican')
                        | (new_data['CUISINE DESCRIPTION'] == 'Italian') | (new_data['CUISINE DESCRIPTION'] == 'Thai')]


    # Convert the 'INSPECTION DATE' values to pandas datetime type and set this column as index
    new_data['INSPECTION DATE'] = pd.to_datetime(new_data['INSPECTION DATE'])

    final_data = new_data.set_index(['INSPECTION DATE'])

    return final_data

'''
This function is used to calculate the total number of certain Cuisine type in the partial_dataset
It returns a list of two lists, suggesting the numbers of each Cuisine type
'''

def Calc_num_each_cuisine(partial_dataset):

    num_list = []
    type_list = ['Korean', 'Indian', 'Chinese', 'Mexican', 'Italian', 'Thai']
    for type in type_list:
        num_list.append(len(partial_dataset[partial_dataset['CUISINE DESCRIPTION'] == type]))

    return [type_list, num_list]

'''
This function calculate the percentage of failed restaurants and passed restaurants for each cuisine type
The two given variables passed_dataset, failed_dataset are supposed to be generated by Calc_num_each_cuisine function.
For example:
passed_dataset=Calc_num_each_cuisine(Passed)
failed_dataset=Calc_num_each_cuisine(Failed)
'''
def Calc_perc_each_cuisin(passed_dataset, failed_dataset):

    passed_perc = []
    failed_perc = []

    for i in range(6):
        passed_perc.append(float(passed_dataset[1][i])/(passed_dataset[1][i]+failed_dataset[1][i]))
        failed_perc.append(1.0 - passed_perc[i])

    return [passed_perc, failed_perc]






