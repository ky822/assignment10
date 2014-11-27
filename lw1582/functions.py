import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_df(path):
  '''cleans dataframe, removes grades that are not A,B, or C; removes restaurants with date 1/1/1900, and all fields that are labeled "Missing"
  sorts the data frame by grade date
  adds a new column YEAR to data frame using grade date
  '''
  df = pd.read_csv(path,sep=',',error_bad_lines = False,index_col = False,dtype = unicode)
  x = ['Not Yet Graded','Z','P','1/1/1900','Missing']
  for i in x:
    df.replace(i,np.nan,inplace = True)
  df_new = df.dropna(axis = 0)
  df_select = df_new[['CAMIS','BORO', 'ZIPCODE','CUISINE DESCRIPTION', 'INSPECTION DATE', 'SCORE', 'GRADE', 'GRADE DATE']]
  df_sorted = df_select.sort(columns = "GRADE DATE")
  df_sorted['YEAR'] = df_sorted['GRADE DATE'].str[-4:].astype(int)
  return df_sorted

def test_grades(grade_list):
  '''question 3: calculates whether the grade of a restaurant has gotten worse or improved over time
  i'm using a simple method of subtracting the first grade from the last grade as an estimate for improvments in restaurant grade over time'''
  grade_point = {'A':4,'B':3,'C':2}

  final_grade = grade_point[grade_list[-1]]
  initial_grade = grade_point[grade_list[0]]
  if final_grade > initial_grade:
    return 1
  elif final_grade < initial_grade:
    return -1
  else:
    return 0

def test_restaurant_grades(df,camis_id):
  '''question 4'''
  restaurant_df = df[(df.CAMIS == camis_id)]
  return test_grades(restaurant_df['GRADE'].tolist())

def plotPDF(boro,df):
  '''question 5: plots the number of restaurants in a boro with each grade over time'''
  plt.figure()
  ind = np.arange(5)

  plt.bar(ind,df['C'],color = 'r', label = 'C')
  plt.bar(ind,df['B'],color = 'b',bottom = df['C'],label = 'B')
  plt.bar(ind,df['A'],color = 'g',bottom = df['C'] + df['B'],label = 'A')
  plt.ylabel('GRADE')
  plt.xticks(ind,('2010','2011','2012','2013','2014'))
  plt.title('Historical Restaurant Grades: ' + boro)
  plt.legend(loc = 'upper left')
  plt.savefig('grade_improvement_' + boro + '.pdf',format = 'pdf')
  plt.close()

def restaurant_count(df):
  '''calculates the number of restaurants by borough over time'''
  boro_list = pd.unique(df.BORO.values.ravel()).tolist()
  year_list = sorted(pd.unique(df.YEAR.values.ravel()).tolist())
  boro_restaurant_count = pd.DataFrame(index = year_list, columns = boro_list)
  for boro in boro_list:
    for year in year_list:
      boro_year_df = df[(df['BORO'] == boro) & (df['YEAR'] == year)]
      count = len(pd.unique(boro_year_df.CAMIS.values.ravel()).tolist())
      boro_restaurant_count.loc[year,boro] = count

  return boro_restaurant_count

def plt_restaurant_count(df):
  '''plot the number of restaurants by borough over time'''
  fig = plt.figure()
  ax = fig.add_subplot(111)
  N = 5
  ind = np.arange(N)
  width = 0.1
  
  rects_1 = ax.bar(ind,df['BRONX'],width,color='r',label = "Bronx")
  rects_2 = ax.bar(ind+width,df['BROOKLYN'],width,color='y',label = "Brooklyn")
  rects_3 = ax.bar(ind+width*2,df['MANHATTAN'],width,color='b',label = "Manhattan")
  rects_4 = ax.bar(ind+width*3,df['QUEENS'],width,color='g',label = "Queens")
  rects_5 = ax.bar(ind+width*4,df['STATEN ISLAND'],width,color='m',label = "Staten Island")
  
  ax.set_ylabel('COUNT')
  ax.set_xticks(ind+width*2)
  ax.set_xticklabels(('2010','2011','2012','2013','2014'))
  ax.legend(loc = "upper left")
  plt.savefig('Number of Restaurants by Boro by Year.pdf',format = 'pdf')
  plt.close()

def plt_cuisine (df):
  '''plot the ten most common cuisines in nyc'''
  plt.figure()
  cuisine_df = df[['CAMIS','CUISINE DESCRIPTION']].drop_duplicates(subset = ['CAMIS'])
  cuisine_counts = cuisine_df.groupby(['CUISINE DESCRIPTION']).size()
  cuisine_counts.sort()
  total_count = cuisine_counts.sum()
  top10 = cuisine_counts[-10:]
  other_count = cuisine_counts[:-10].sum()
  top10['Other'] = other_count
  index = [i.decode('utf8').encode('ascii','replace') for i in top10.index]
  plt.pie(top10/total_count,labels = index,autopct='%1.1f%%')
  plt.savefig('Restaurant Count by Cuisine.pdf',foramt = 'pdf')
  plt.close()