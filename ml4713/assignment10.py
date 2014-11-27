# -*- coding: utf-8 -*-
"""Assignment 10
   Mengfei Li
"""

from ass10 import *


def main():
    
    #read the data and clean it
    dat=pd.read_csv('/Users/mengfeili/Desktop/Programming_for_DS/ml4713/nyc_res.csv')
    dat=dat[(dat.GRADE.notnull())&(dat.GRADE!='Not Yet Graded')&(dat.GRADE!='P')&(dat.GRADE!='Z')]

    #sum of grades over all restaurant 
    print 'sum grade over all restaurant: ', total_grade(dat)
    
    #sum of grade for each boroughs
    print 'sum grade for BRONX: ', grade_boro('BRONX',dat)
    print 'sum grade for QUEENS: ', grade_boro('QUEENS',dat)
    print 'sum grade for BROOKLYN: ', grade_boro('BROOKLYN',dat)
    print 'sum grade for STATEN: ', grade_boro('STATEN ISLAND',dat)
    print 'sum grade for MANHATTAN: ', grade_boro('MANHATTAN',dat)
    
       
    #barplots for nyc and five boroughs: 'BRONX','BROOKLYN','MANHATTAN','QUEENS','STATEN ISLAND'
    nyc_dat=g_date(dat)
    nyc=grade_over_time(nyc_dat)
    nyc.plot(kind='bar',title='grade_improvement_nyc')
   
    bronx_dat=g_date(dat.iloc[np.where(dat.BORO=='BRONX')])
    bronx=grade_over_time(bronx_dat)
    bronx.plot(kind='bar',title='grade_improvement_bronx')
    
    queens_dat=g_date(dat.iloc[np.where(dat.BORO=='QUEENS')])    
    queens=grade_over_time(queens_dat)
    queens.plot(kind='bar',title='grade_improvement_queens')

    brooklyn_dat=g_date(dat.iloc[np.where(dat.BORO=='BROOKLYN')])    
    brooklyn=grade_over_time(brooklyn_dat)
    brooklyn.plot(kind='bar',title='grade_improvement_brooklyn')

    manhattan_dat=g_date(dat.iloc[np.where(dat.BORO=='MANHATTAN')])
    manhattan=grade_over_time(manhattan_dat)
    manhattan.plot(kind='bar',title='grade_improvement_manhattan')


    staten_dat=g_date(dat.iloc[np.where(dat.BORO=='STATEN ISLAND')])
    staten=grade_over_time(staten_dat)
    staten.plot(kind='bar',title='grade_improvement_staten')

    #additional analysis 
    n=10
    n_most_name,n_values=top_n_cuisine(dat,n)
    n_cuisine_name_graph(n,n_most_name,n_values)
    
    
    cuisine_grade_A,cuisine_grade_B,cuisine_grade_C=sum_grade_cuisine(dat) 
    top_n_A=[cuisine_grade_A[n_most_name[i]] for i in range(n)]
    n_cuisine_grade(top_n_A,n_most_name,n)
    top_n_B=[cuisine_grade_B[n_most_name[i]] for i in range(n)]
    n_cuisine_grade(top_n_B,n_most_name,n)
    top_n_C=[cuisine_grade_C[n_most_name[i]] for i in range(n)]
    n_cuisine_grade(top_n_C,n_most_name,n)




if __name__=='__main__':
    main()    