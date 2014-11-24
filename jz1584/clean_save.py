import pandas as pd

def cleanGrade(dataset):
    """function cleans up the data by removing all entries that have invalid grades 
    including NaN, save the dataFrame to new csv file called 'clean.csv'
    """
    df=pd.read_csv(dataset)
    grades=['A','B','C']
    row_mask=df.GRADE.isin(grades) 
    df2=df[row_mask]
    df2.to_csv('clean.csv',index=False)


#def createDateFrame():
if __name__=="__main__":
    cleanGrade('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
    