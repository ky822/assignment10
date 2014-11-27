import numpy as np
import pandas as pd
def Run(raw_data):
	'''
	Answer to Question 2
	'''
	def data_clean(df):
		'''
		This function selects required columns, drops invalid rows and transforms dates.
		
		Returns a cleaned new data frame'''
		df_new = df[['BORO', 'CUISINE DESCRIPTION', 'GRADE', 'GRADE DATE']]
		df_new = df_new[pd.notnull(df_new['GRADE']) & pd.notnull(df_new['GRADE DATE']) & (df_new['GRADE']!='Not Yet Graded') & (df_new['GRADE']!='P') &  (df_new['GRADE']!='Z')]    
		df_new['GRADE DATE'] = pd.to_datetime(df_new['GRADE DATE'])
		df_new = df_new.drop_duplicates()
		return df_new
	print '\n-------------------Answer to question 2 -------------------'
	print '\nData cleaning...'
	data = data_clean(raw_data)
	print '\nData cleaned...'
	return data
	
