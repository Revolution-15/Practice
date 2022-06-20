import numpy as np
import random
from itertools import product

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