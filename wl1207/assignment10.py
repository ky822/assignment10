import pandas as pd
from function import *

def main():
	
	try:
		BORO_list = ['NYC','BRONX','QUEENS','BROOKLYN','MANHATTAN','STATEN ISLAND']
		
		#Question4:
		print 'This is the answer for Question4.'
		for BORO in BORO_list:
			print 'The sum of restaurant grades in {} is : {}'.format(BORO,sum_grades(BORO))
		
		#Question5:
		print 'This is the answer for Question5.'
		for BORO in BORO_list:
			print 'Generate the graph for {} '.format(BORO)
			GraphNumberofRestaurant(BORO)
		
		#Question6:
		print 'This is the answer for Question6.' 
		print 'More information about the data. '
		
		print 'Save pie graph for grades.'
		pieGraph_Grade()
		
		print 'Save pie graph for top 8 cuisine types. '
		pieGraph_CuisineDescription()
		
	except(KeyboardInterrupt,EOFError):
		print 'Quit.'
	
		
if __name__=='__main__':
	main()