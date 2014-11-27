import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')

#First, clean the data.

df = df[['CAMIS','BORO','GRADE DATE','GRADE','CUISINE DESCRIPTION']] # Only these five columns are relevant to the analysis.
df = df.dropna() #Drop all records having NA in columns.
df = df[df['GRADE'].isin(['A','B','C'])] #Drop GRADE that is 'Z' or 'P'.
df['GRADE DATE'] = pd.to_datetime(df['GRADE DATE']) #Transform the GRADE DATE to datetime format.

def pieGraph_Grade():
	
	'''
	This function will give six subplots in one pdf, each subplot displays the pie graph of 'GRADE' in each BORO.
	'''
	
	BORO_list = ['NYC','BRONX','QUEENS','BROOKLYN','MANHATTAN','STATEN ISLAND']
	fig = plt.figure()
	
	for i in range(len(BORO_list)):
		if BORO_list[i]=='NYC':
			instance = df[:]
		else:
			instance = df[df['BORO']==BORO_list[i]]
		
		plt.subplot(2,3,i)
		instance['GRADE'].value_counts().plot(kind='pie',colormap='gist_rainbow',autopct='%.2f',fontsize=9)
		plt.title('{}'.format(BORO_list[i]))
	
	plt.savefig('pieGraph for grade in Boroughs.pdf')
	plt.clf()

def pieGraph_CuisineDescription():
	'''
	This function will give six subplots in one pdf, each subplot displays the pie graph of 'CUISINE DESCRIPTION' in each BORO.
	And because there are 85 types, we only display top 8 of them.
	'''
	BORO_list = ['NYC','BRONX','QUEENS','BROOKLYN','MANHATTAN','STATEN ISLAND']
	fig = plt.figure()
	
	for i in range(len(BORO_list)):
		if BORO_list[i]=='NYC':
			instance = df[:]
		else:
			instance = df[df['BORO']==BORO_list[i]]
		
		plt.subplot(2,3,i)
		instance['CUISINE DESCRIPTION'].value_counts()[:8].plot(kind='pie',colormap='gist_rainbow',fontsize=9)
		plt.title('{}'.format(BORO_list[i]))
	
	plt.savefig('pieGraph for top 8 cuisine type in boroughs.pdf')
	plt.clf()


def GraphNumberofRestaurant(BORO):
	
	if BORO=='NYC':
		instance = df[:]
	else:
		instance = df[df['BORO']==BORO]
		
	for i in ['A','B','C']:
		sub = instance[instance['GRADE']==i]
		sub.groupby(by='GRADE DATE')['GRADE'].count().plot(label=i)
	
	plt.title('Total number of restaurants in {}'.format(BORO))
	plt.legend()
	plt.savefig('grade_improvement_{}.pdf'.format(BORO))
	plt.clf()	
	

def test_grades(grade_list):

	'''Using linear regression model.
	if the slope > 0.2, consider it as improving and return 1; 
	else if the slope < - 0.3, consider it as declining and return -1;
	else, consider it as remaining and return 0.
	In order to do this, we also have to map the categories 'A','B','C' into numbers[1,0,-1].
	In reality, the threshold should be set base on past experience.
	'''
	
	mapping = {'A':1,'B':0,'C':-1}
	grade_list_mapping = map(lambda x: mapping[x], grade_list)
	
	#Linear regression.
	if len(grade_list_mapping) >1 :
		# If our grade list has more than one grade, we could see its change overtime ; 
		# otherwise, the change, represented by slope, should be set to 0.
		y = np.array(grade_list_mapping)
		x = np.array(range(len(grade_list_mapping)))
		A = np.vstack([x,np.ones(len(x))]).T
		slope = np.linalg.lstsq(A,y)[0][0]
	else:
		slope = 0
	
	if slope > 0.2:
		grade = 1
	elif slope < -0.3:
		grade = -1
	else:
		grade = 0
		
	return grade
	
def test_restaurant_grades(camis_id):

	# For each camis_id, select out its records in df.
	instance = df[df['CAMIS']==camis_id]
	
	# Sort the records according to its 'GRADE DATE' order. 
	instance.sort_index(by='GRADE DATE',ascending=True)
	
	#In order to call the test_grades function, we can only pass list as parameter
	grade_list = list(instance['GRADE'])
	
	return test_grades(grade_list)

def sum_grades(BORO):

	if BORO == 'NYC':
		camis_list = list(df['CAMIS'].unique())
	
	else:
		# Select out all records in that BORO.
		# And get the camis list.
		instance = df[df['BORO']==BORO]
		camis_list = list(instance['CAMIS'].unique())
	
	#Sum the grades for all restaurant in given borough.
	sum_grade = sum([test_restaurant_grades(x) for x in camis_list])
	
	return sum_grade
	