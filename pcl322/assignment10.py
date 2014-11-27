from mod.grad import *
from sets import Set
import pandas as pd
import numpy as np

if __name__ == "__main__":

	print "========== Part 1 =========="
	print "Dataset downloaded.\n"


	print "========== Part 2 =========="
	data_path = "DOHMH_New_York_City_Restaurant_Inspection_Results.csv"
	df = pd.DataFrame.from_csv(data_path)
	df = clean_up_dataset(df)
	print "Dataset loaded and cleaned.\n"


	print "========== Part 3 =========="
	print "Function created."
	print "Justification saved as part3.txt\n"


	print "========== Part 4 =========="
	#Compute the sum of scores of the city and the five boroughs
	result = compute_sum(df)
	#Write the result
	fp = open("part4.txt", "w")
	fp.write(result.to_string())
	fp.close()
	print "Result saved as part4.txt\n"


	print "========== Part 5 =========="
	#Plot the graphs of NYC and five boroughs
	generate_graphs(df)
	print "Figures saved as required."
	print "Conclusion saved as part5.txt\n"


	print "========== Part 6 =========="
	#Analyze the number of types of violation during all time
	violation_analysis(df)
	print "Figures saved as part_*.png"
	print "Analysis saved as part6.txt\n"


