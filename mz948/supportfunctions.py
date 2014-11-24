import matplotlib.pyplot as plt

def grade_transform(grade_letter):
    '''
    This function transforms letter of grades into integers
    'A' will be transformed to 1, B -- 2, C -- 3, D -- 4, ..., Z -- 26
    '''
    grade_letter = ord(grade_letter.lower()) - 96
    grade_letter = int(grade_letter)
    return grade_letter

def grade_list_transform(grade_list):
    '''
    This function transforms a list of grades into a list of integer numbers
    '''
    num_list = []
    for grade in grade_list:
        grade = grade_transform(grade)
        num_list.append(grade)
    return num_list

       
def grade_plot(df,name):
    '''This function generates plot with arguments of a dataframe and its name''' 
    df = df.groupby(['GRADE DATE','GRADE']).size()
    df = df.unstack().fillna(0)
    plt.figure(figsize=(12,5))
    plt.plot(df.index, df['A'],'r', label = 'A')
    plt.plot(df.index, df['B'],'k', label = 'B')
    plt.plot(df.index, df['C'],'c', label = 'C')
    plt.plot(df.index, df['P'],'g', label = 'P')
    plt.plot(df.index, df['Z'],'m', label = 'Z')
    plt.title('Number of Restaurants with Different Grades in ' + name +' Over Time')
    plt.xlabel('Time')
    plt.ylabel('Number of Restaurants')
    plt.legend(loc = 'upper left')
    plt.savefig('grade_improvement_'+ name + '.pdf')
    
