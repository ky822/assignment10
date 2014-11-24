import pandas as pd
'''
It is a function to make the GRADE DATE column as format as the python system recongnize 
format like year-month-day
use pd.datetime to convert
'''
def format_date(list_d):
    #get the value of year
    year=[int(x[-4:]) for x in list_d]
    #get the value of month
    month=[int(x[:2]) for x in list_d]
    #get the value of day
    day=[int(x[3:5]) for x in list_d]
    #change to date time format
    date=[pd.datetime(year[i],month[i],day[i]) for i in xrange(len(year))]
    return date