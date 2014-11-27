__author__ = 'chianti'

from funcs_assign10 import *

def main():

    # Since df=PreprocessingData(), data is the cleaned data set we need
    # It only contains four columns: 'CAMIS', 'BORO', 'GRADE', 'GRADE DATE'
    data = df

    if 0 == 0:
    # Use a dictionary to store the grade for each CAMIS id.
    # The grade is calculated by test_restaurant_grades(camis_id)
        each_id_grades = {}

        camis_id_list = list(set(data.CAMIS))

        for camis_id in camis_id_list:
            each_id_grades[camis_id] = test_restaurant_grades(camis_id)
            # each_id_grades is like: {41484288: 1, 41265836: 0, 41353218: 1, 41680924: 0, 41156640: 1, ... }

    if 1 == 1:   # Question 4
    # compute the sum of test_restaurant_grades(camis_id) over all restaurants in the data set
        sum_grades = np.sum(each_id_grades.values())
        print 'The sum of test_restaurant_grades(camis_id) over all restaurants: \n', sum_grades


    if 2 == 2:   # Question 4
    # compute the sum of test_restaurant_grades(camis_id) for each of the five Boroughs.
        boro_grades = {}

        for boroughs in ['STATEN ISLAND', 'BROOKLYN', 'BRONX', 'MANHATTAN', 'QUEENS']:
            # Get a list of CAMIS IDs from each borough
            each_boro_camis_id_list = list(set(data[data.BORO == boroughs].CAMIS))

            # Calculate the grade for each CAMIS ID
            grades = [each_id_grades[each_camis_id] for each_camis_id in each_boro_camis_id_list]
            boro_grades[boroughs] = np.sum(grades)

        print 'The sum of test_restaurant_grades(camis_id) in each borough is: \n', boro_grades

    if 3 == 3:  # Question 5a
    # Generate a graph that shows the total number of restaurants in NYC for each grade over time
        Plot_Grades_Over_Time(data, 'nyc')

    if 4 == 4:   # Question 5b
    # Generate one graph for each of the five Boroughs that shows the total number of restaurants in the Borough for
    # each grade over time.
        for boroughs in ['STATEN ISLAND', 'BROOKLYN', 'BRONX', 'MANHATTAN', 'QUEENS']:
            boro_data = data[data.BORO == boroughs]
            Plot_Grades_Over_Time(boro_data, boroughs)


    if 5 == 5:   # Question 6
    # As an illustration to analysis the relationship between a restaurant's cuisine type and sanitary score, I only use
    # part of the data set with CUISINE DESCRIPTION as Korean, Indian, Chinese, Mexican, Italian, and Thai.

        # Use PreprocessingCuisineData() to generate the DataFrame we need in this question
        CUISINEdata = PreprocessingCuisineData()

        # Since SCORE >=28 means a restaurant failed the inspection, separate CUISINEdata into two parts, one with
        # information of the restaurants who passed the inspection, and one with the information who failed.
        Passed = CUISINEdata[CUISINEdata.SCORE < 28]
        Failed = CUISINEdata[CUISINEdata.SCORE >= 28]

        # Calculate the total number of restaurant for each CUISINE TYPE in the Passed and Failed data sets.
        Passed_num = Calc_num_each_cuisine(Passed)
        Failed_num = Calc_num_each_cuisine(Failed)

        # Calculte the percentage of failed restaurants and passed restaurants for each cuisine type
        PassFail_perc = Calc_perc_each_cuisin(Passed_num, Failed_num)

        # Convert the data we've got to a DataFrame, which is easy to plot
        to_plot_df = pd.DataFrame(columns=['Passed', 'Failed'], index=['Korean', 'Indian', 'Chinese', 'Mexican',
                                                                       'Italian', 'Thai'])
        to_plot_df['Passed'] = np.array(PassFail_perc[0])
        to_plot_df['Failed'] = np.array(PassFail_perc[1])

        # Plot the figure to show the percentage of failed inspection and passed inspection for six cuisine types
        to_plot_df.plot(kind='bar', stacked=True)
        plt.title('Percentage of failed inspection and passed inspection')
        plt.xticks(rotation=30)
        plt.xlabel('Cuisine Description')
        plt.ylabel('Percentage')
        plt.savefig('Question6.pdf')
        plt.show()













if __name__ == '__main__':
    main()

