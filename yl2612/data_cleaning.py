import pandas as pd

def clean_data_q2(df):
    '''
    This function clean up the data as required by question 2.
    '''
    clean_df = df[['CAMIS', 'BORO', 'GRADE', 'GRADE DATE']] #select the columns that will be used for assessment
    clean_df = clean_df.dropna() #remove rows with missing data
    clean_df = clean_df[clean_df.GRADE != 'Not Yet Graded'] #remove rows having 'Not yet Graded' in the 'GRADE' column
    clean_df = clean_df[clean_df.GRADE != 'P']  #remove rows having 'P' in the 'GRADE' column
    clean_df = clean_df[clean_df.GRADE != 'Z']  #remove rows having 'Z' in the 'GRADE' column
    clean_df = clean_df.drop_duplicates() #drop duplicated rows
    clean_df['GRADE DATE'] = pd.to_datetime(clean_df['GRADE DATE']) #convert string to date for the 'GRADE DATE' column
    clean_df = clean_df.set_index('CAMIS') #set the row labels using the 'CAMIS' column
    return clean_df


def process_data_q5(df):
    '''
    Generate a data frame for grade, with row index as 'GRADE DATE' and column index as 'CAMIS' id.
    '''
    li_date=[]
    unique_date = df['GRADE DATE'].unique() #select the unique dates
    for date in unique_date:
        date_df = df[df['GRADE DATE'] == date] #create a data frame for each unique date
        create_dict = dict(zip(date_df.index, date_df['GRADE']))
        li_date.append(create_dict) #create a list of dictionaries
        
    date_grade_id = pd.DataFrame(data=li_date) #change the list to a data frame
    date_grade_id = date_grade_id.set_index(unique_date)
    date_grade_id = date_grade_id.fillna(method='ffill') #fill missing with the last observed grade in each column
    
    return date_grade_id


def process_data_q6(df):
    '''
    Clean up the data for question 6.
    Return a data frame with cuisine description as row label and the number of restaurants as column label
    '''   
    cuisine_df = df[['CAMIS', 'CUISINE DESCRIPTION']] #select columns that will be used for q6
    cuisine_df = cuisine_df.dropna()
    cuisine_df = cuisine_df.drop_duplicates()
    cuisine_df = cuisine_df.set_index('CAMIS')
    count_num = cuisine_df.apply(pd.Series.value_counts, axis=0) #count the number of cuisines
    count_num.columns =['Count'] #change the column name
    count_num = count_num.sort('Count',ascending=False) #sort the data frame with the largest count on top.
    return count_num


def selector(df, num_range):
    '''
    Select the data above a certain number range.
    Return a data frame with the number of restarurants larger than the specfied number range
    '''
    new_df = df[df['Count'] > num_range]#create a new df with 'Count' larger than the specfied number range
    return new_df
