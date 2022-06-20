#!/usr/bin/env python

import os
import sys
from math import sqrt
import time

import random
#from utils import communicate
from itertools import product
#
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

#from plexe import Plexe, ACC, CACC

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



VEHICLE_LENGTH = 4
DISTANCE = 6  # inter-vehicle distance
LANE_NUM = ['a_1','a_2','a_3','b_1','b_2','b_3','c_1','c_2','c_3','d_1','d_2','d_3']
PLATOON_SIZE = 1
SPEED = 16.6  # m/s
V2I_RANGE = 200 
PLATOON_LENGTH = VEHICLE_LENGTH * PLATOON_SIZE + DISTANCE * (PLATOON_SIZE - 1)
ADD_PLATOON_PRO_EW = 0.5
ADD_PLATOON_PRO_NS = 0.5
ADD_PLATOON_STEP = 300
#MAX_ACCEL = 2.6
#DECEL = SPEED**2/(2*(V2I_RANGE-25))  
#DECEL = 3.5
STOP_LINE = 15.0


def return_routeID(x):
    #print(x)
    if x[0]=='a' and x[2]=='1':
        return('1')
    elif x[0]=='a' and x[2]=='2':
        return('2')
    elif x[0]=='a' and x[2]=='3':
        return('3')
    elif x[0]=='b' and x[2]=='1':
        return('4')
    elif x[0]=='b' and x[2]=='2':
        return('5')
    elif x[0]=='b' and x[2]=='3':
        return('6')
    elif x[0]=='c' and x[2]=='1':
        return('7')
    elif x[0]=='c' and x[2]=='2':
        return('8')
    elif x[0]=='c' and x[2]=='3':
        return('9')
    elif x[0]=='d' and x[2]=='1':
        return('10')
    elif x[0]=='d' and x[2]=='2':
        return('11')
    elif x[0]=='d' and x[2]=='3':
        return('12')
    #print("im still here")


def lanes(x):
    if x=='a':
        return 'e1'
    elif x=='b':
        return 'e2'
    elif x=='c':
        return 'e3'
    elif x=='d':
        return 'e4'

def randomise():
    n = random.randint(4,10)
    return n
        
    
def add_single_platoon(step, lane):

    vid = "v.%d.%s.%d" %(step/ADD_PLATOON_STEP, lane[0], int(lane[2]))
    num = return_routeID(lane)
    #print(lane)
    routeID = "route_" + num  
    dl = lanes(lane[0])
    #print(dl)
    n=randomise()
    traci.vehicle.add(vid, routeID, typeID="vtypeauto")
    traci.vehicle.setSpeedMode(vid, 31)        
    traci.vehicle.setSpeed(vid, n)
    traci.vehicle.setColor(vid, (255,0,0, 255))  # red
    #topology.append(vid)
        


def add_platoons(step):
    for lane in LANE_NUM:    # lane a,b,c,d
        if lane == 'a_1' or lane == 'a_2' or lane == 'a_3' or lane == 'c_1' or lane == 'c_2' or lane == 'c_3': 
            if random.random() < ADD_PLATOON_PRO_NS:
                add_single_platoon(step, lane)
        if lane == 'b_1' or lane == 'b_2' or lane == 'b_3' or lane == 'd_1' or lane == 'd_2' or lane == 'd_3':
            if random.random() < ADD_PLATOON_PRO_EW:
                add_single_platoon(step, lane)

def nonzero(x):
    count = 0
    for i in x:
        if i!=0:
            count+=1
    return count


def conversion(input):
    initial_list = [0, 0, 0, 0]
    input_list_ids=[0, 0, 0, 0]
    for veh in input:
        lane_id = veh.split(".")[2]
        fut_man = veh.split(".")[3]
        if lane_id == 'a':
            initial_list[0] = 'a_'+ fut_man
            input_list_ids[0] = veh
        elif lane_id == 'b':
            initial_list[1] = 'b_'+ fut_man
            input_list_ids[1] = veh
        elif lane_id == 'c':
            initial_list[2] = 'c_'+ fut_man
            input_list_ids[2] = veh
        elif lane_id == 'd':
            initial_list[3] = 'd_'+ fut_man
            input_list_ids[3] = veh
    return initial_list,input_list_ids

def compar(a,b):
    c=[0,0,0,0]
    #print(a)
    #print(b)
    if b[0]!=0:
        c[0]=a[0] 
    if b[1]!=0:
        c[1]=a[1]
    if b[2]!=0:
        c[2]=a[2]
    if b[3]!=0:
        c[3]=a[3]
    #print(c)
    return c

all_zeros = [0, 0, 0, 0]
#########################################################################################################
def my_algorithm(input):
    first_list = []
    for i in input:
        if i!=0:
            temporary = [input[0], input[1], input[2], input[3]]
            for j in temporary:    
                if i!=j and j!=0:
                    if j in conflict_matrix[i]:
                        #print(j)
                        ind = temporary.index(j)
                        temporary[ind] = 0
            first_list.append(temporary)
        if i == 0:
            first_list.append(all_zeros)
    #print(first_list) 
    if first_list == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]:
        return
    #-------------------
    count = []
    for x in first_list:
        #print(x)
        n = nonzero(x)
        count.append(n)
        #print(count)
    
    
    max_count = max(count)
    z = count.index(max_count)
    #print(z)

    first_output = first_list[z]
    
    #print(first_output)
    
    #---------------------
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
    #------------------------

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
################################################################################################

def main():

    sumo_cmd = ['sumo-gui', '--duration-log.statistics', '--tripinfo-output', 'my_output_file.xml', '-c', 'my_confg.sumo.cfg']
    traci.start(sumo_cmd)
    
    step = 0
    topology = []
    serving_list = []  
    action_list = []
    #output_list_ids=[]

    while step < 360000:  # 1 hour       

        traci.simulationStep()

        if step % ADD_PLATOON_STEP == 0:  # add new platoon every X steps
            add_platoons(step) 
        
        topology=list(traci.vehicle.getIDList())
        print(step,'__________________________________________________________________')
        c=0

        

        for veh in topology:            
            odometry = traci.vehicle.getDistance(veh)
            if (veh not in serving_list) and (492-30 <= odometry < 492-6): 
                serving_list.append(veh)
                traci.vehicle.setSpeed(veh, 4.0) 
            # if (veh in serving_list) and (492-10 <= odometry < 492-6): 
            #     traci.vehicle.setSpeed(veh, 1.0)  
            if (508<odometry) and (veh in serving_list):
                serving_list.remove(veh)

        #serving_list[:] = [element for element in serving_list if element in topology] 

        for veh in topology:
            odometry = traci.vehicle.getDistance(veh)
            if (492 - 6 <= odometry <= 492) :

                if (veh not in output_list_ids):
                    traci.vehicle.setSpeed(veh, 0.0)
                    print("Nahi jaunga", veh)

                if veh not in action_list:
                    action_list.append(veh)
                
                if (veh in output_list_ids) and (veh in action_list):
                    traci.vehicle.setSpeed(veh, 10.0)
                    print("First... ja na l***", veh)
            
            if (odometry > 492) and (veh in action_list):
                action_list.remove(veh)

            if odometry>492:
                traci.vehicle.setSpeed(veh,10.0)

            if (492 < odometry <= 508):
                #traci.vehicle.setSpeed(veh,10.0)
                c+=1
                

        input_list , input_list_ids = conversion(action_list) # to make in ordered form from action list to input_list_ids

        print('action_list',action_list)
        #print(input_list_ids)
        
        if c==0:
            #output_list_ids = [0, 0, 0, 0]
            output_list = my_algorithm(input_list)
            if output_list==None:
                output_list=[0,0,0,0]
            output_list_ids = compar(input_list_ids , output_list)

        print('output_list_ids',output_list_ids)
        print(c)

        for veh in output_list_ids:
            if veh!=0:
                traci.vehicle.setSpeed(veh, 10.0)
                #print(veh)
                print("tisra... Ja bhai", veh)


        step += 1

    traci.close()


if __name__ == "__main__":
    main()
        
