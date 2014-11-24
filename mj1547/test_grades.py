def test_grades(grade_list):
    '''
    It is a test_grades function which is based on the GRADE list
    '''
    #grade_list=df.GRADE
    #set intital value
    value=0
    '''
    since the date was decreasing compare I Will campare the list from last to firsr
    and when the grade from A to B, the grade will be -1 and the grade change from A to A
    the value do not change, and when the value change from B to A or C to B, the value will +1
    and for my justification:
    1) the total value for each restaurant is small then 0, the grade is decling , and return -1
    2) when the total value is 0, keep the same,return 0
    3) when the total value is bigger then 0,improving, return 1
    '''
    #get the total value of each cimas list
    for i in range(len(grade_list)-1):
        if grade_list[i] < grade_list[i+1]:
            value=value+1
        if grade_list[i] > grade_list[i+1]:
            value=value-1
        else:
            value=value+0
    #return the 1,0,-1 to represent improve, keep same, and decling for each list
    if int(value)<0:
        value = -1
    if int(value)==0:
        value = 0
    elif int(value)>0:
        value = 1
    return value