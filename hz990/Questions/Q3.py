import numpy as np
import pandas as pd


def Run():
	print '\n-------------------Answer to question 3 -------------------'
	print 'The function \'test_grades(grade_list)\' that Question 3 is asking for can be found in Q3.py'



def test_grades(grade_list):
    '''
    This function takes a list of grades as input.
    A cumulative variable 'cumu_score' is set to compute the final value.
    If next grade is better than previous one, cumu_score + 1.
    If next grade is equal to previous one, cumu_score stays the same.
    If next grade is worse than previous one, cumu_score - 1
    
    Return:
    If cumu_score == 0, returns 0.
    If cumu_score > 0, returns 1.
    If cumu_score < 0, returns -1
    '''
    if len(grade_list) == 1:
        final_score = 0
    else:
        data = map(ord, grade_list)
        cumu_score = 0
        for i in xrange(len(data)-1):
            if data[i+1] < data[i]:
                cumu_score +=1
            elif data[i+1] > data[i]:
                cumu_score -=1
            else:
                continue
        if cumu_score > 0:
            final_score = 1
        elif cumu_score == 0:
            final_score = 0
        else:
            final_score = -1
    return final_score                
