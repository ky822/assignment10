import sys
import numpy as np

# Question 3
def test_grades(grade_list, reverse=False):
    """ test whether a list of grades has an increasing trend by fit a linear regression model to it """
    n = len(grade_list)
    if n == 1:
        return 0
    x = np.arange(0, 2, 2./n)
    A = np.array([x, np.ones(n)])
    grade_dict = {'A': 2, 'B': 1, 'C': 0}
    try:
        y = [grade_dict[g] for g in grade_list]
    except KeyError as e:
        sys.exit('There should only be 3 levels of grades: A, B, or C')
    w = np.linalg.lstsq(A.T, y)[0]
    
    # We got the 0.375 magic number by assuming the sequence A, B, B, B, A, A, A has an increasing trend
    if w[0] > 0.375:
        trend = 1
    elif w[0] < -0.375:
        trend = -1
    else:
        trend = 0
    return -trend if reverse else trend

def test_restaurant_grades(df, camis_id):
    """ Check if the specified restaurant has an improving trend """
    # Get the list of grades sorted by date
    grade_list = list(df.GRADE[df.index==int(camis_id)])
    return test_grades(grade_list, reverse=True)
