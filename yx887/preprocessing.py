import pandas as pd

def house_keeping(df):
    """ Data cleaning """
    gradings = df[['CAMIS', 'BORO', 'GRADE', 'GRADE DATE']]    # only need 4 cols
    gradings = gradings[(gradings.GRADE=='A') | (gradings.GRADE=='B') | (gradings.GRADE=='C')]
    gradings = gradings.drop_duplicates()
    gradings['GRADE DATE'] = pd.to_datetime(gradings['GRADE DATE'])    # change data type to datetime
    return gradings.set_index('CAMIS')

def house_keeping_v2(df):
    """ Data cleaning for question 6 """
    new_df = df[['CAMIS', 'BORO', 'CUISINE DESCRIPTION']]
    new_df = new_df.drop_duplicates()
    new_df.columns = ['CAMIS', 'BORO', 'DESCRIPTION']
    return new_df
