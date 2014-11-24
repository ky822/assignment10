import time
from datetime import date, datetime, time
from sets import Set
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt


def clean_up_dataset(df):
	#Filter out the useless records (invalid boroughs and grades)
	return df[(df["BORO"] != "Missing") & ((df["GRADE"] == "A") | \
			(df["GRADE"] == "B") | (df["GRADE"] == "C"))]

def quantified(list):
	#Construct the mapping table
	mapping = {"A":4, "B":3, "C":2}

	return [mapping[i] for i in list]

def test_grades(grade_list):

	#For those who were graded only once, test_grade is 0
	if len(grade_list) == 1:
		return 0

	#Translate A B C into 4 3 2 
	q_grade_list = quantified(grade_list)

	#If there are only two grades, the test_grade can be determined easily
	if len(grade_list) == 2:
		if q_grade_list[1] - q_grade_list[0] > 0:
			return 1
		elif  q_grade_list[1] - q_grade_list[0] < 0:
			return -1
		else:
			return 0

	#If there are more than three grades, compute the 2nd order polynomial regression for it
	linear_fit = np.polyfit(range(len(q_grade_list)), q_grade_list, 2)

	#Determine test_grade by the slope of the poly fit on the last grade date
	if 2*linear_fit[0]*(len(q_grade_list)-1)+linear_fit[1] < -0.1:
		return -1
	elif 2*linear_fit[0]*(len(q_grade_list)-1)+linear_fit[1] > 0.1:
		return 1
	else:
		return 0


def test_restaurant_grades(df, camis_id):

	#For those who were graded only once, test_grade is 0
	if len(df["GRADE"][camis_id]) == 1:
		return 0

	#Get the record of GRADE and GRADE DATE for ID=camis_id
	grade_list = list(df["GRADE"][camis_id])
	date_list = list(df["GRADE DATE"][camis_id])

	#Translate the dates into date format
	date_list = [datetime.strptime(d, '%m/%d/%Y') for d in date_list]

	#Sort the grades by its dates
	merged = zip(grade_list, date_list)
	merged = sorted(merged, key = lambda m: m[1])

	#Return the test_grade for the grades
	return test_grades(grade_list)


def count_ABC(list):

	#Translate A B C into 4 3 2
	#Add one A B C in the list to prevent the zero count
	added_list = quantified(list+["A", "B", "C"])
	#Count the number of A B C in the list
	counts = np.bincount(added_list)

	return counts[4]-1, counts[3]-1, counts[2]-1


def generate_boro_graphs(df, boro_label):

	#Get all the grade dates and sort them
	dates_time = sorted([datetime.strptime(d, "%m/%d/%Y") for d in list(Set(df["GRADE DATE"]))])
	#Translate the dates into string format
	dates_str = [d.strftime("%m/%d/%Y") for d in dates_time]

	#Set GRADE DATE as index and retrieve CAMIS and GRADE
	df_didx = df.reset_index().set_index("GRADE DATE")[["CAMIS", "GRADE"]]

	#Create the pools for each restaurants of each grade
	set_ABC = {"A":Set([]), "B":Set([]), "C":Set([])}

	#lists ABC are for plotting
	list_A = []
	list_B = []
	list_C = []
	#For each date in order compute the numbers of ABC
	for d in dates_str:
		#Remove duplicated rows
		record_on_d =  df_didx.loc[d].drop_duplicates()

		#For series and dataframe do different list initialization
		if type( record_on_d ) is not pd.core.series.Series:
			restaurants = record_on_d["CAMIS"].tolist()
			grades = record_on_d["GRADE"].tolist()
		else:
			restaurants = [record_on_d["CAMIS"]]
			grades = [record_on_d["GRADE"]]
		
		for i in range(len(restaurants)):
			#Remove the restaurant from the pool (the previous grade can be either A B C)
			set_ABC["A"].discard(restaurants[i])
			set_ABC["B"].discard(restaurants[i])
			set_ABC["C"].discard(restaurants[i])
			#Add the restaurant to the pool according to updated grade
			set_ABC[grades[i]].add(restaurants[i])

		#Record the number for plotting
		list_A.append(len(set_ABC["A"]))
		list_B.append(len(set_ABC["B"]))
		list_C.append(len(set_ABC["C"]))

	#Plots
	fig, ax = plt.subplots(figsize=(12, 6))
	ax.plot(dates_time, list_A, label = "Garde A")	
	ax.plot(dates_time, list_B, label = "Grade B")	
	ax.plot(dates_time, list_C, label = "Garde C")	
	ax.set_title(boro_label)
	ax.set_ylabel("Number of Restaurants")
	ax.legend( loc="upper left" )

	plt.savefig("grade_improvement_%s.pdf" % (boro_label.lower().split(" ")[0]), format="pdf")
	plt.close()


def generate_graphs(df):

	#Get all the boroughs
	boro = df["BORO"].unique()

	#Plot for NYC
	generate_boro_graphs(df, "NYC")
	#Plot for the five boroughs
	for b in boro:
		generate_boro_graphs(df[df["BORO"] == b], b)


def compute_sum(df):
        #Create the empty dataframe for the result
        boroughs = df["BORO"].unique()
        result = pd.DataFrame(index=list(boroughs)+["NYC"], columns=["Sum"])

        #Compute the sum of scores of NYC
        sum = 0
        for id in list(Set(df.index)):
                sum = sum + test_restaurant_grades(df, id)
        result["Sum"]["NYC"] = sum

        #Compute the sum of scores of five boroughs
        for b in boroughs:
                df_boro = df[df["BORO"]==b]

                sum = 0
                for id in list(Set(df_boro.index)):
                        sum = sum + test_restaurant_grades(df_boro, id)
                result["Sum"][b] = sum

        return result


def violation_boro_analysis(df, vio_codes, boro_label):

	#Compute the counts of different codes
	counts = []
	for v in vio_codes:
		counts.append( len(df[df["VIOLATION CODE"] == v]) )

	#Plot
	fig, ax = plt.subplots()
	fig.set_size_inches(25,10)

	width = 1.0
	ax.bar(np.arange(len(vio_codes)), counts, width)
	ax.set_title(boro_label)
        ax.set_xticks(np.arange(len(vio_codes))+0.5*width)
        ax.set_xticklabels(vio_codes, rotation=80)
        ax.set_ylabel("Number of Restaurants")

	plt.savefig("part6_%s" % (boro_label.split(" ")[0]))
	plt.close()


def violation_analysis(df):

	#Get all the kinds of violation codes and remove the null
	vio_codes = df["VIOLATION CODE"][pd.notnull(df["VIOLATION CODE"])].unique()

	#Counts the number of appearance and plot
	violation_boro_analysis(df, vio_codes, "NYC")

	#Get all the boroughs
	boro = list(Set(df["BORO"]))
	for b in boro:
		violation_boro_analysis(df[df["BORO"] == b], vio_codes, b)


