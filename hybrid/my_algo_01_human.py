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

human  ='a_3'

def nonzero(x):
    count = 0
    for i in x:
        if i!=0:
            count+=1
    return count

all_zeros = [0, 0, 0, 0]

def loop(new):
    ##################################################################################
    # first_list = []
    # for i in new:
    #     if i!=0:
    #         temporary = [new[0], new[1], new[2], new[3]]
    #         for j in temporary:    
    #             if i!=j and j!=0 :
    #                 if j in conflict_matrix[i]:
    #                     #print(j)
    #                     ind = temporary.index(j)
    #                     temporary[ind] = 0
    #         first_list.append(temporary)
    #     if i == 0:
    #         first_list.append(all_zeros)
    # #print(first_list) 
    # if first_list == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]:
    #     return
    # #-------------------
    # count = []
    # for x in first_list:
    #     #print(x)
    #     n = nonzero(x)
    #     count.append(n)
    #     #print(count)
    

    # max_count = max(count)
    z = None
    for i in new:
        if i!=0 and i!=human:
            if i in conflict_matrix[human]:
                ind = new.index(i)
                new[ind]=0

    if human in new:
        z = new.index(human)
    print(z)

    first_output = new
    
    #print(first_output)
    
    ####################################################################################
    second_list = []
    for i in first_output:
        if i!=first_output[z] and i!=0:
            temp2 = [first_output[0], first_output[1], first_output[2], first_output[3]]

            for j in temp2:
                if i!=j and j!=z and j!=0:
                    if j in conflict_matrix[i]:
                        ind = temp2.index(j)
                        temp2[ind] = 0
            second_list.append(temp2)
        if i == 0 or i == first_output[z]:
            second_list.append(all_zeros)
    #print(second_list)

    if second_list == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]:
        return first_output
    #---------------------
    count2 = []
    for x in second_list:
        #print(x)
        n = nonzero(x)
        count2.append(n)
        #print(count)

    max_count2 = max(count2)
    z2 = count2.index(max_count2)
    #print(count2)
    #print(z2)
    
    second_output = second_list[z2]
    
    #print(second_output)

    # if first_output == second_output:
    #    return second_output
    ####################################################################################

    third_list = []
    for i in second_output:
        if i!=first_output[z] and i!=0 and i!=second_output[z2]:
            temp3 = [second_output[0], second_output[1], second_output[2], second_output[3]]

            for j in temp3:
                if i!=j and j!=z and j!=0 and j!=z2:
                    if j in conflict_matrix[i]:
                        ind = temp3.index(j)
                        temp3[ind] = 0
            third_list.append(temp3)
        if i == 0 or i == first_output[z] or i == second_output[z2]:
            third_list.append(all_zeros)
    #print(third_list)

    if third_list == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]:
        return second_output
    #---------------------
    count3 = []
    for x in third_list:
        #print(x)
        n = nonzero(x)
        count3.append(n)
        #print(count)

    max_count3 = max(count3)
    z3 = count3.index(max_count3)
    #print(z3)

    third_output = third_list[z3]

    #print(third_output)

    if second_output == third_output:
        return third_output
    else:
        return third_output
    #####################################################################################


if __name__ == "__main__":
    # j=0
    # while j<300:
    #     j+=1
    #     randomlist = []
    #     for i in range(0,4):
    #         n = random.randint(0,3)
    #         randomlist.append(n)
    #     print(j,randomlist,"random list")
    #     original = randomlist
    #     original = [str(original[0]), str(original[1]), str(original[2]), str(original[3])]
    #     new = ["a_"+original[0], "b_"+original[1], "c_"+original[2], "d_"+original[3]]
    #     for i in range(4):
    #         if randomlist[i] == 0:
    #             new[i] = 0
    #     print(loop(new), 'is the output')
    #     print( )

    j=0
    for roll in product([0, 1, 2, 3], repeat = 4):
        j+=1
        roll = list(roll)
        #print(j, roll)  

        original = roll
        original = [str(original[0]), str(original[1]), str(original[2]), str(original[3])]
        new = ["a_3", "b_"+original[1], "c_"+original[2], "d_"+original[3]]
        #print(j, new)
        for i in range(1,4):
            if roll[i] == 0:
                new[i] = 0
        print(j, new)
    # new = list(input("enter the part: "))

        print(loop(new), "is the output")
        print()

        