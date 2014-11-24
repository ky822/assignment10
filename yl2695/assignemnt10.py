from functions import *

def main():
    '''
    main function of this assignment
    '''

    # problem2
    print '-------------Problem2-------------'
    print 'Try to read data from file and clean the data.'
    try:
        df = cleanData()
    except:
        print 'Something is wrong with the file!'
    print

    # problem4
    print '-------------Problem4-------------'
    df = df.set_index('CAMIS')
    uniqueIndex = df.index.unique()
    totalGrades = 0
    for index in uniqueIndex:
        totalGrades += test_restaurant_grades(df, index)
    print 'The total grades of the NYC is:', totalGrades
    borough = ['BRONX', 'BROOKLYN', 'QUEENS', 'MANHATTAN', 'STATEN ISLAND']
    for area in borough:
        grades = 0
        dfNew = df[df['BORO'] == area]
        uniqueIndex = dfNew.index.unique()
        for index in uniqueIndex:
            grades += test_restaurant_grades(dfNew, index)
        print 'The total grades of {} is:'.format(area), grades

    # problem5
    print '-------------Problem5-------------'
    print 'Please see attached pdf files which shows the total number of restaurants of each grades.'
    plotTotalGrades()
    plotEachBorough()

    # problem6
    print '-------------Problem6-------------'
    print 'Please see attached graph showing the total scores of the inspection of each restaurant.'
    showScore()

if __name__ == '__main__':
    main()
