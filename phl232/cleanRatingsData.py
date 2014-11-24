import pandas as pd

'''

Script to clean NYC restaurant inspection data

https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/xx67-kt59

'''

# Read Data

filePath = 'inspectionResults.csv'
inspectionResultsRaw = pd.read_csv(filePath)

# Clean Data

dropNames = ['DBA', 'BUILDING', 'STREET', 'ZIPCODE', 'PHONE', 'ACTION', 'VIOLATION CODE', 
'VIOLATION DESCRIPTION', 'CRITICAL FLAG', 'INSPECTION DATE', 'RECORD DATE', 'INSPECTION TYPE', 'SCORE']

inspectionResultsRaw = inspectionResultsRaw.drop(dropNames, axis = 1).dropna()
inspectionResultsRaw = inspectionResultsRaw.drop_duplicates()
inspectionResultsRaw['GRADE DATE'] = pd.to_datetime(inspectionResultsRaw['GRADE DATE'])
inspectionResultsRaw = inspectionResultsRaw.drop_duplicates()

# Save dataframe

inspectionResultsRaw.to_pickle('inspectionResultsRaw')


