from supportingfunction import *


def test_restaurant_grades(df, camis_id):
    shop_grade = df.ix[camis_id].GRADE
    test = test_grades(shop_grade)
    return test


def main():

    #Problem 1 & 2 & 3
    document = 'DOHMH_New_York_City_Restaurant_Inspection_Results.csv'
    data = import_clean_data(document)
    data.index = data.CAMIS

    #Problem 4 & 5: The quality of the restaurants in City of New York generally improved.
    gradeplot(data, 'nyc')
    all_id = list(set(data.index))
    for boro in ['BRONX', 'QUEENS', 'BROOKLYN', 'MANHATTAN', 'STATEN ISLAND']:
        gradeplot(data[data.BORO == boro], boro.lower().split(' ')[0])
        print boro+': ' + str(np.sum([test_restaurant_grades(data, x) for x in list(set((data[data.BORO == boro]).index))]))
        all_grade = [test_restaurant_grades(data, x) for x in all_id]
        print 'All city: '+ str(np.sum(all_grade))


    #Problem 6: We can use this data to see top 10 restaurant cuisines in NYC.
    #This data is useful for assessing the quality of quality of restaurants in NYC.
    data2 = data[['CAMIS','CUISINE DESCRIPTION']].drop_duplicates(subset=['CAMIS'])
    cui_size = data2.groupby(['CUISINE DESCRIPTION']).size()
    cui_size.sort()
    total_num = cui_size.sum()
    top10 = cui_size[-10:]
    top10_num = top10.sum()
    other_num = cui_size[:-10].sum()
    top10['Other'] = other_num
    index = top10.index
    index = [x.decode('utf8').encode('ascii','replace') for x in index]
    plt.figure()
    plt.pie(top10/total_num, labels = index, autopct='%1.1f%%', shadow = True)
    plt.axis('equal')
    plt.savefig('Pie Chart.png')



if __name__ == '__main__':
    main()


