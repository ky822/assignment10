# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 21:59:35 2014

@author: LaiQX
"""
from functions import *

def main():
    raw_data = pd.read_csv('DOHMH_New_York_City_Restaurant_Inspection_Results.csv')
    data = data_clean(raw_data)
    grade_test_count(data)
    grade_plot(data, 'NYC')
    group_boroughs = data.groupby('BORO')
    for name, groups in group_boroughs:
        grade_plot(groups, name)
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass