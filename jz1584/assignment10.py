import pandas as pd
from gradeTesting import sum_boroGrade
from gradeTesting import test_grades
from clean_save import cleanGrade
from visulization import plotGradeTrend




 

if __name__=="__main__":
    cleanGrade('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
    NYC_df=pd.read_csv('clean.csv')
    NYC_df['GRADE DATE']=pd.to_datetime(NYC_df['GRADE DATE'])#change the string type of date to 'date' type 
    test_grades(['A','B','A','B'])
    sum_boroGrade()
    
    bronx_df=NYC_df[NYC_df.BORO=='BRONX']#
    bklyn_df=NYC_df[NYC_df.BORO=='BROOKLYN']
    manhat_df=NYC_df[NYC_df.BORO=='MANHATTAN']
    queens_df=NYC_df[NYC_df.BORO=='QUEENS']
    Staten_df=NYC_df[NYC_df.BORO=='STATEN ISLAND']
    
    plotGradeTrend(NYC_df,'NYC')
   
    plotGradeTrend(bronx_df,'BROOKLYN')
    plotGradeTrend(bronx_df,'BRONX')
    plotGradeTrend(bronx_df,'MANHATTAN')
    plotGradeTrend(bronx_df,'QUEENS')
    plotGradeTrend(bronx_df,'STATEN ISLAND')
    
    

    
    
   
     
     
    
    
    
