'''
Created on Nov 24, 2014

@author: keye
'''

from Questions.Load_Cleanup_Data import *
from Questions.Finish_Question3 import *
from Questions.Compute_Print_Sum_of_Grade import *
from Questions.Plot_Number_of_Restaurants_for_Grade import *
from Questions.Plot_Percentage_of_Cuisines import *

def main():
    """
    Solve the questions of the assignment.
    
    1.Import the dataset 'DOHMH_New_York_City_Restaurant_Inspection_Results.csv' into a pandas DataFrame. Clean up the data, for example, by removing all entries that have invalid grades (in the 'GRADE' column).
    
    2.Write a function called test_grades(grade_list) to calculate if a list of grades are improving or not.
    
    3.Write the function called test_restaurant_grades(camis_id) to examine if the grades improves, declines or stay the same over time. 
      Compute and print out the sum of test_restaurant_grades(camis_id) over all restaurants and for each of the five Boroughs.
    
    4.Generate a graph that shows the total number of restaurants in New York City for each grade and one graph for each of the five Boroughs that shows the total number of restaurants in the Borough for each grade over time.
    
    5.Generate a graph to show the percentages of the top 10 cuisines so that we can make an assumption on the favors of customers.
    
    """
    
    #Questions 1&2: Import the database into a pandas DataFrame and clean up the data. for example, by removing all entries that have invalid grades (in the 'GRADE' column).
    NYCRestaurantInspection, Raw_NYCRestaurantInspection = Load_Cleanup_Data() 
    
    #Questions 3: Write a function called test_grades(grade_list) to calculate if a list of grades are improving or not.
    Finish_Question3()
    
    #Questions 4: Write the function called test_restaurant_grades(camis_id) to examine if the grades improves, declines or stay the same over time. Compute and print out the sum of test_restaurant_grades(camis_id) over all restaurants and for each of the five Boroughs.
    Compute_Print_Sum_of_Grade(NYCRestaurantInspection)
    
    #Question 5: Generate a graph that shows the total number of restaurants in New York City for each grade and one graph for each of the five Boroughs that shows the total number of restaurants in the Borough for each grade over time.
    Plot_Number_of_Restaurants_for_Grade(NYCRestaurantInspection)
    
    #Question 6: Generate a graph to show the percentages of the top 10 cuisines so that we can make an assumption on the favors of customers.
    Plot_Percentage_of_Cuisines(Raw_NYCRestaurantInspection)   
       
if __name__ == '__main__':
    main()
