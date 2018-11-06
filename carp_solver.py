# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    carp_solver.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Corey <390583019@qq.com>                   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/11/06 11:17:19 by Corey             #+#    #+#              #
#    Updated: 2018/11/06 14:31:52 by Corey            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import random
import time
import sys
import getopt


SEED = 0 
random.seed(SEED)
INS_FILE_PATH = sys.argv[1]
opts,args = getopt.getopt(sys.argv[2:],"t:s:")
for op, value in opts:
    if  op == '-t':
        TERMINATION  = value
    if  op == '-s':
        SEED = value


def main():
    ins_name = ""
    vetices = 0
    depot = 0
    task = 0
    non_task = 0
    vehicle = 0
    capicity = 0
    total_cost = 0
    tcost = 0
    count = 0
    try:
        f = open(INS_FILE_PATH)
        ins_name = f.readline().split(':')[1].strip() # the name of instance
        vetices = f.readline().split(':')[1].strip() # the number of vertices
        depot = f.readline().split(':')[1].strip() # the depot vertex
        task = f.readline().split(':')[1].strip() # the number of tasks(required edges)
        non_task = f.readline().split(':')[1].strip() # the number of non-required edges
        vehicle = f.readline().split(':')[1].strip() # the number of vehicles
        capicity = f.readline().split(':')[1].strip() # the capicity of vehicles
        total_cost = f.readline().split(':')[1].strip() # the total cost of all tasks
        # print(ins_name,total_cost)
        
        f.readline() # description (useless)
        for line in f:
            if line == 'END':
                print(line),
            else:
                
                node1, node2, cost, demand = map(int,line.split())
                if demand != 0:
                    tcost += (cost)
                    count += 1
                pass
        print(tcost,count)
    except IOError:
        print("File not found! Please check your instance file path.")
        pass
    finally:
        f.close()
    pass

class node():
    def __init__(self,id):
        self.id = id
        self.visited = False
    
    def add(self,parameter_list):
        pass

class graph():
    pass

main()
