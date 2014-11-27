import pandas as pd
import string

def clean_data():
    """
    Function that will clean up the raw data set
    """
    df=pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')  # read in data
    df=df[pd.notnull(df['GRADE'])]  # drop rows with grades missing
    df=df[pd.notnull(df['GRADE DATE'])]  # drop rows with grade date missing
    df=df[df.GRADE != 'P']  # drop rows whose grade are P
    df=df[df.GRADE != 'Z']  # drop rows whose grade are Z
    df=df[df.GRADE != 'Not Yet Graded']  # drop rows whose grade are Not Yet Graded
    df=df[df.BORO != 'Missing']  # drop rows whose Borough information is missing
    df['GRADE DATE']=pd.to_datetime(df['GRADE DATE'])  # convert string date time to python datetime format
    return df

def test_grades(grade_list):
    """
    Function that takes in a list of grades and calculate whether the restaurant is improving, declining or unchanging
    
    The intuition of this method is to check grades iteratively. Say a total score of zero at begining. If improving, then add 1.
    
    If declining, then minus 1. If unchanging, then do nothing. After comparing every grades in the list iteratively, it will have a sum.
    
    Positive, Negative or Zero. If positive, then improving. If negative, then declining. If zero, then unchanging.
    """
    value = lambda x: string.ascii_uppercase.index(x)+1  # mapping uppercase letters to integers starting from 1
    j=0  # initialize three values to store improving, declining or unchanging increments
    k=0
    l=0
    for i in range(len(grade_list)-1):  # do comparison between every elements in the list until the last one
        if value(grade_list[i+1]) > value(grade_list[i]):
            j+=-1  # if declining and letter index gets larger, then minus 1
        elif value(grade_list[i+1]) == value(grade_list[i]):
            l+=0  # if unchanging and letter index keep the same, then do nothing
        elif value(grade_list[i+1]) < value(grade_list[i]):
            k+=1  # if improving and letter index gets smaller, then plus 1
    if j+k+l > 0:
        return 1  # if the sum is positive, then it is improving, return 1
    elif j+k+l == 0:
        return 0  # if the sum is zero, then it is not changing, return 0
    elif j+k+l < 0:
        return -1  # if the sum is negative, then it is declining, return -1

def test_restaurant_grades(camis_id, df):
    """
    Function that takes in a particular camis_id and returns if the restaurant is improving, declining, or unchanging.
    """
    df=df[df.CAMIS==camis_id]  # subset the data with particular camis_id
    return test_grades(df['GRADE'].iloc[::-1].values.tolist())  # using the above function to calculate the index of improving, declining, or unchanging
                                                                # using the grades in ascending order by date
def plot_nyc(df):
    """
    Function that plots the total numbere of restaurants in NYC and five boroughs for each grade over time.
    """
    df=df.groupby(['GRADE DATE', 'GRADE'])  # subset the dataframe with only grade and grade date
    df=pd.DataFrame(df.size().unstack().fillna(0))  # transform the object into tabular with each grade counts, also fill in missing value with 0
    df.plot()  # using the built in dataframe plot function
    

	


