import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
pd.set_option('display.mpl_style', 'default')
import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = (16.0, 10.0)

def grade_count(df):
	'''
	This function returns a new DataFrame with date as index and number of each grade as colums.
	'''
	tmp = []
	date_index = sorted(list(df['GRADE DATE'].unique()))
	for date in date_index:
		df_11 = df[df['GRADE DATE'] <= date] #Select sub-DataFrame with same date
		df_11['CAMIS'] = df_11.index
		df_12 = df_11.sort(columns='GRADE DATE', ascending=False) # Sort by date
		df_1 = df_12.drop_duplicates(['CAMIS'])# Drop duplicates in order to count
		grade_count_tmp = []
		for grade in ['A', 'B', 'C']:
			df_2 = df_1[df_1.GRADE == grade] #Select same grade
			num = len(list(df_2.index.unique())) #Count grade number
			grade_count_tmp.append(num)
		tmp.append(grade_count_tmp)
	# Return the new DataFrame
	df_new = pd.DataFrame(tmp, index=date_index, columns=['A', 'B', 'C'])
	return df_new

def plot_grade(df, name):
	'''
	This function plots the required graphs.
	'''
	plt.figure()
	y = np.row_stack((df.C, df.B, df.A))
	x = df.index
	fig, ax = plt.subplots()
	sp = ax.stackplot(x, y)
	plt.title('Total {} restaurants for each grade over time'.format(name))
	plt.ylabel('Number of Restaurants')
	proxy = [mpl.patches.Rectangle((0,0), 0,0, facecolor=pol.get_facecolor()[0]) for pol in sp]
	ax.legend(proxy,('Grade C', 'Grade B', 'Grade A'), loc='upper left')
	plt.grid('off')
	plt.savefig('grade_improvement_' + name.lower().split(' ')[0] + '.pdf')

def Run(data):
	print '\n-------------------Answer to question 5 -------------------\n'
	print 'Generating \'grade_improvement_nyc.pdf\'...'
	df_nyc = grade_count(data)
	plot_grade(df_nyc, 'nyc') #Plot nyc first

	for name in ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND']:
		df1 = data[data.BORO == name]
		df2 = grade_count(df1)
		print 'Generating \'grade_improvement_{}.pdf\'...'.format(name.lower().split(' ')[0])
		plot_grade(df2, name)
	print '\nThe conclusion for question 5 can be seen in \'conclusion_Q5.txt\'\n'
