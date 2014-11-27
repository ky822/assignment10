from functions import *
import pandas as pd

def main():
  df = clean_df("NYC_Restaurant_Results.csv")

  '''get the list of boroughs from dataframe'''
  boro_list = pd.unique(df.BORO.values.ravel()).tolist()
  
  '''question 4: for each borough, calculates whether restaurant grades have been worsening or improving over time'''
  boro_grade = {}
  for boro in df.BORO.unique():
    grade = 0
    boro_df = df[(df.BORO == boro)]
    for camis in boro_df.CAMIS.unique():
      grade += test_restaurant_grades(boro_df,camis)
      boro_grade[boro] = grade
    boro_grade['nyc'] = sum(boro_grade.values())

  print "test_restaurant_grades for the 5 boros: \n"
  print boro_grade

  '''question 5: plots for each borough and new york city the number of restaurants for each grade over time'''
  for boro in boro_list:
    boro_df = df[df.BORO == boro]
    boro_year_df = boro_df.groupby(['YEAR','GRADE']).size().unstack()
    plotPDF(boro,boro_year_df)
  
  year_df = df.groupby(['YEAR','GRADE']).size().unstack()
  plotPDF("NYC",year_df)

  '''question 6: plot the distribution of restaurants by cuisine'''
  plt_cuisine(df)
  
  '''question 6: plots the number of restaurants in each borough over time'''
  count = restaurant_count(df)
  plt_restaurant_count(count)

if __name__ == '__main__':
  main()
