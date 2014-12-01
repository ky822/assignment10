'''
Created on Nov 24, 2014

@author: keye
'''

from Questions.Question2 import *
from Questions.Question3 import *
from Questions.Question4 import *
from Questions.Question5 import *
from Questions.Question6 import *

def main():
    """
    Solve the questions of the assignment.
    """
    
    #Questions 1&2: Import the database into a pandas DataFrame and clean up the data. for example, by removing all entries that have invalid grades (in the 'GRADE' column).
    NYCRestaurantInspection, Raw_NYCRestaurantInspection = Question2() 
    #Questions 3: Write a function called test_grades(grade_list) to calculate if a list of grades are improving or not.
    Question3()
    #Questions 4: Write the function called test_restaurant_grades(camis_id) to examine if the grades improves, declines or stay the same over time. Compute and print out the sum of test_restaurant_grades(camis_id) over all restaurants and for each of the five Boroughs.
    Question4(NYCRestaurantInspection)
    #Generate a graph that shows the total number of restaurants in New York City for each grade and one graph for each of the five Boroughs that shows the total number of restaurants in the Borough for each grade over time.
    Question5(NYCRestaurantInspection)
    #Generate a graph to show the percentages of the top 10 cuisines so that we can make a assumption for the favors of customers.
    Question6(Raw_NYCRestaurantInspection)   
       
if __name__ == '__main__':
    main()

    




 
    



