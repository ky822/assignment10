import pandas as pd
from test_grades import test_grades
def test_restaurant_grades(df_resturant,camis_id):   
    '''
    It is a function to calculate the value for each restautant 
     '''
    df_perresturant=df_resturant.ix[camis_id]
   
    df = list(df_perresturant['GRADE'])
   
    return test_grades(df)