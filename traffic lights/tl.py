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
ADD_PLATOON_PRO_EW = 0.3
ADD_PLATOON_PRO_NS = 0.3
ADD_PLATOON_STEP = 1200
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
    traci.vehicle.setColor(vid, (255,255,255, 255))  # red
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
    for veh in input:
        traci.vehicle.setSpeed(veh, 1.0)
        lane_id = veh.split(".")[2]
        fut_man = veh.split(".")[3]
        if lane_id == 'a':
            initial_list[0] = 'a_'+ fut_man
        elif lane_id == 'b':
            initial_list[1] = 'b_'+ fut_man
        elif lane_id == 'c':
            initial_list[2] = 'c_'+ fut_man
        elif lane_id == 'd':
            initial_list[3] = 'd_'+ fut_man
    return initial_list


def main():

    sumo_cmd = ['sumo-gui', '--duration-log.statistics', '--tripinfo-output', 'my_output_file.xml', '-c', 'my_confg.sumo.cfg']
    traci.start(sumo_cmd)
    # traci.simulationStep()plexe 
    #plexe = Plexe()

    #traci.addStepListener()
    
    step = 0
    topology = []
    serving_list = []  
    action_list = []
    #initial_list = [0,0,0,0]

 
    while step < 360000:  # 1 hour       

        traci.simulationStep()

        if step % ADD_PLATOON_STEP == 0:  # add new platoon every X steps
            add_platoons(step) 
        
        topology=list(traci.vehicle.getIDList())
        print(step,'__________________________________________________________________')
        #print(step)
        deleted_veh = []
        for veh in topology:            
            odometry = traci.vehicle.getDistance(veh)
            if (not veh in serving_list) and (492-30 <= odometry < 492-15): 
                serving_list.append(veh)
                #traci.vehicle.setSpeed(veh, 4.0)
            if (veh in serving_list) and (492-15 <= odometry < 492-6): 
                #serving_list.append(veh)
                #traci.vehicle.setSpeed(veh, 1.0)  
                print('sushant')    

        
        #print("topology =",topology )
   
        #print("serving_list =", serving_list)

        serving_list[:] = [element for element in serving_list if element in topology]  


        for veh in serving_list:
            odometry = traci.vehicle.getDistance(veh)
            if (492 - 6 < odometry < 492) and veh not in action_list:
                action_list.append(veh)
                #traci.vehicle.setSpeed(veh, 0.0)

            elif (odometry > 492) and (veh in action_list):
                #print(veh)
                action_list.remove(veh)
        

        #print("Action_list_dist = " ,action_list)

        #temp=[]

        step += 1

    traci.close()


if __name__ == "__main__":
    main()
        
