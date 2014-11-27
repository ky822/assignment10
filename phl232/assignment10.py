# -*- coding: utf-8 -*-
"""

Script for HW 10

"""

import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import grade


##############################################################################
# Get Data
##############################################################################
dataName = 'inspectionResultsRaw'
inspectionResultsRaw = pd.read_pickle(dataName)

# Inspection results indexed by ID
gradeByID = inspectionResultsRaw.set_index('CAMIS')
gradeByID = gradeByID[gradeByID['GRADE'].isin(list('ABC'))]

# Inspection results indexed by Grade Data
gradeByTime = inspectionResultsRaw.drop(['CUISINE DESCRIPTION'], axis = 1)
gradeByTime = gradeByTime.drop_duplicates()


##############################################################################
# Script to get answers
##############################################################################

# Question 4

print ' --------Question 4 -------- \n'
    
idList = gradeByID.index.unique()
improvement = [grade.test_restaurant_grades(gradeByID, x) for x in idList ] 

gradeImprovement = pd.DataFrame(improvement, idList)
gradeImprovement = gradeImprovement.join(gradeByID['BORO'])
gradeImprovement.columns = ['Improvement', 'BORO']

groupedImprovement = gradeImprovement.groupby('BORO').sum()

groupedImprovement = groupedImprovement.drop('Missing')
groupedImprovement.loc['NYC'] = gradeImprovement.Improvement.sum()

print groupedImprovement

# Question 5, graphs

print ' --------Question 5 -------- \n'
print 'Generating Charts ... \n'

boroList = ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND', 'NYC']

for boro in boroList:

    graphDF = grade.getGradeCountByTime(gradeByTime, boro)
    graphDF[['A', 'B', 'C']].plot(title = 'Count of Restaurant Health Grades in ' + boro)
    print boro + 'done'
    
#    # Save Histogram
#    outName = 'grade_improvement_' + boro.lower()
#    pp = PdfPages(outName+'.pdf')
#    pp.savefig()
#    pp.close()

# Question 6, something interesting

print ' --------Question 6 -------- \n'

print ' Using this data, we can examine the average rating by cuisine \n'

averageRatings = gradeByID['GRADE'].replace({'A': 3, 'B': 2, 'C': 1}).groupby(gradeByID.index).mean()
averageRatings = pd.concat([averageRatings, gradeByID['CUISINE DESCRIPTION']], axis = 1).drop_duplicates()
groupedByCuisine = averageRatings.groupby('CUISINE DESCRIPTION').mean()
groupedByCuisine = groupedByCuisine.sort('GRADE', ascending = False)


print '\n Top 5'
print groupedByCuisine.head()


print '\n Worst 5'
print groupedByCuisine.tail()

print '\n * A = 3, B = 2, C = 1'