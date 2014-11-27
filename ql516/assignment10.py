# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 21:59:35 2014

@author: LaiQX
"""
import pandas as pd
import sys
from functions import *

def main():
    while 1:    
        file_path = raw_input("Please input the relative path of the csv dataset file: ")  
        try:
            raw_data = pd.read_csv(file_path)
            break
        except (KeyboardInterrupt,EOFError):
            sys.exit()
        except IOError:
            print "Not a valid path name, please try again, or you can use <C-C> or <C-D> to interrupt this program"

    #or you can just put the data in the same directory of this .py script and uncomment the next line
    #and the whole while loop above
    #raw_data = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
    
    
    #Clean the data
    data = data_clean(raw_data)
    
    #count the grade of NYC and Each Boroughs
    grade_test_count_all(data)
    grade_test_count(data)
    
    # Plot the improvement 
    print "Ploting... it will take 5 ~ 7 minutes, you can press <C-C> or <C-D> to interrupt"
    grade_plot(data, 'NYC')
    group_boroughs = data.groupby('BORO')
    for name, groups in group_boroughs:
        grade_plot(groups, name)
    
if __name__ == '__main__':
     try:
         main()
     except (KeyboardInterrupt,EOFError):
         pass