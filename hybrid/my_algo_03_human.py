import numpy as np
import random
from itertools import product

conflict_matrix = {
    'a_3':['b_3', 'b_1', 'c_1', 'd_3', 'd_2', 'd_1'], 
    'a_2':['b_3', 'c_1'], 
    'a_1':['b_3', 'b_1', 'c_3', 'c_2', 'c_1', 'd_3', 'd_1'], 
    'b_3':['a_3', 'a_2', 'a_1', 'c_3', 'c_1', 'd_1'], 
    'b_2':['c_3', 'd_1'], 
    'b_1':['a_3', 'a_1', 'c_3', 'c_1', 'd_3', 'd_2', 'd_1'],
    'c_3':['a_1', 'b_3', 'b_2', 'b_1', 'd_3', 'd_1'],
    'c_2':['a_1', 'd_3'],
    'c_1':['a_3', 'a_2', 'a_1', 'b_3', 'b_1', 'd_3', 'd_1'],
    'd_3':['a_3', 'a_1', 'b_1', 'c_3', 'c_2', 'c_1'],
    'd_2':['a_3', 'b_1'],
    'd_1':['a_3', 'a_1', 'b_3', 'b_2', 'b_1', 'c_3', 'c_1']
    }
#print(conflict_matrix['a_2'])

#print(new)

human = 'a_2'
human2 = 'b_2'
human3 = 'c_2'


def nonzero(x):
    count = 0
    for i in x:
        if i!=0:
            count+=1
    return count

all_zeros = [0, 0, 0, 0]

def loop(new):
    ##################################################################################
    
    z = None
    for i in new:
        if i!=0 and i!=human and i!=human2 and i!=human3:
            if i in conflict_matrix[human] or i in conflict_matrix[human2] or i in conflict_matrix[human3]:
                ind = new.index(i)
                new[ind]=0

    if human in new:
        z = new.index(human)

    if human2 in new:
        zt = new.index(human2)

    if human3 in new:
        zz = new.index(human3)
    
    first_output = new
    
    #print(first_output)
    return first_output
    ####################################################################################
    
    #####################################################################################


if __name__ == "__main__":
    
    j=0
    for roll in product([0, 1, 2, 3], repeat = 4):
        j+=1
        roll = list(roll)
        #print(j, roll)  
        original = roll
        original = [str(original[0]), str(original[1]), str(original[2]), str(original[3])]
        new = ["a_2", "b_2", "c_2", "d_"+original[3]]
        #print(j, new)
        for i in range(3,4):
            if roll[i] == 0:
                new[i] = 0
        print(j, new)

        print(loop(new), "is the output")
        print()

        