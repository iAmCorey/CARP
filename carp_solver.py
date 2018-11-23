# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    CARP_solver.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Corey <390583019@qq.com>                   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/11/06 11:17:19 by Corey             #+#    #+#              #
#    Updated: 2018/11/22 20:59:55 by Corey            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import random
import time
import sys
import getopt
import heapq
import copy
import numpy as np


SEED = 0 

INS_FILE_PATH = sys.argv[1]
opts,args = getopt.getopt(sys.argv[2:],"t:s:")
for op, value in opts:
    if  op == '-t':
        TERMINATION  = value
    if  op == '-s':
        SEED = value

random.seed(SEED)

def main():
    ins_name = ""
    vertices = 0
    depot = 0
    tasks = 0
    non_tasks = 0
    vehicles = 0
    capacity = 0
    total_cost = 0

    start = time.time()
    try:
        f = open(INS_FILE_PATH)
        ins_name = f.readline().split(':')[1].strip() # the name of instance
        vertices = int(f.readline().split(':')[1].strip()) # the number of vertices
        depot = int(f.readline().split(':')[1].strip()) # the depot vertex
        tasks = int(f.readline().split(':')[1].strip()) # the number of tasks(required edges)
        non_tasks = int(f.readline().split(':')[1].strip()) # the number of non-required edges
        vehicles = int(f.readline().split(':')[1].strip()) # the number of vehicles
        capacity = int(f.readline().split(':')[1].strip()) # the capicity of each vehicle
        total_cost = int(f.readline().split(':')[1].strip()) # the total cost of all tasks
        # print(ins_name,total_cost)

        this_graph = graph(vertices,depot,tasks,non_tasks,vehicles,capacity,total_cost)
        this_graph.addVertex(depot)
        f.readline() # description (useless)
        for line in f:
            if line == 'END':
                pass
                # print(line),
            else:
                
                node1, node2, cost, demand = map(int,line.split())
                new_edge = edge(node1,node2,cost,demand)
                this_graph.addEdge(new_edge)
                
        f.close()


        this_graph.setDistanceMatrix() # use dijkstra's algorithm

        # for debug
        # print(this_graph.getDemandMatrix())
        # print(this_graph.getDistanceMatrix())

        task_list = np.where(this_graph.getDemandMatrix() > 0)
        free = list(zip(task_list[0],task_list[1])) # free 
        # print(free)

        routes = pathScanning(this_graph, free, capacity, depot, 2)
        cost = getCost(this_graph, routes, depot)

        # print(cost)
        # costs = []
        # for i in range(4):
        #     # print(routes)
        #     rule = i+2 
        #     costs.append(pathScanning(this_graph, free, capacity, depot, rule))

        # print(costs) 

        (routes,cost) = flip(this_graph,routes,cost,depot)

        print("s", (",".join(str(d) for d in s_format(routes))).replace(" ", ""))
        print("q", cost)
        print("cost time:", time.time()-start)
        
    except IOError:
        print("File not found! Please check your instance file path.")
        pass
        
    pass




def pathScanning(graph,free,capacity,start,rule):
    k = 0
    route = [[]]
    cost = [0]
    
    while len(free):
        depot = start
        remain_cap = capacity
        k+=1
        route.append([])
        cost.append(0)
        
        # print("free: ", free)
        while (remain_cap >= 0):
            choice = []
            for task in free:
                if graph.getDemandMatrix()[task[0],task[1]] < remain_cap:
                    choice.append(task)
            
            if len(choice):
                choosing_task = ChooseTask(graph, depot, choice, remain_cap, capacity, rule)
                route[k].append(choosing_task)
                # print(choosing_task)
                free.remove(choosing_task)
                free.remove((choosing_task[1],choosing_task[0]))
                remain_cap -= graph.getDemandMatrix()[choosing_task[0],choosing_task[1]]
                depot = choosing_task[1]
            else:
                break
        


    return copy.deepcopy(route[1:])


def ChooseTask(graph, depot, choice, remain_cap, capacity, rule_num):
    distances = {}
    terms = {}
    for each_choice in choice:
        distance = graph.getDistanceMatrix()[depot, each_choice[0]]
        distances[distance] = each_choice
        term = (graph.getDemandMatrix()[each_choice[0],each_choice[1]]) / (graph.getCostMatrix()[each_choice[0],each_choice[1]])
        terms[term] = each_choice
            
    if rule_num == 1:
        choosing = distances[max(distances)]
    elif rule_num == 2:
        choosing = distances[min(distances)]
    elif rule_num == 3:
        choosing = terms[max(terms)]
    elif rule_num == 4:
        choosing = terms[min(terms)]
    elif rule_num == 5:
        
        if remain_cap > 0.5 * capacity:
            # maximize the distance between the task and the depot
            choosing = distances[max(distances)]              
        else:
            choosing = distances[min(distances)]
            # minimize it
    return choosing

def getCost(graph, routes, depot):
    cost = 0
    for route in routes:
        cost += graph.getDistanceMatrix()[depot, route[0][0]] # depot to the first node
        cost += graph.getDistanceMatrix()[depot, route[-1][1]] # back from the final node
        cost += graph.getCostMatrix()[route[0][0], route[0][1]] # the first node's cost

        for i in range(len(route)-1):
            node = route[i]
            next_node = route[i+1]
            cost += graph.getDistanceMatrix()[node[1],next_node[0]] + graph.getCostMatrix()[next_node[0],next_node[1]]

    return cost

def flip(graph, routes, cost, depot):

    for i in range(len(routes)):
        for j in range(len(routes[i])):
            new_routes = copy.deepcopy(routes)
            flip_item = new_routes[i][j]
            new_flip_item = (flip_item[1],flip_item[0])
            flip_item = new_flip_item
            new_routes[i][j] = flip_item

            if getCost(graph, routes, depot) < cost:
                print(new_flip_item)
                routes = new_routes
                cost = getCost(graph, routes, depot)

    return (routes,cost)


def validPath(graph, routes):
    for route in routes:
        capacity = 0
        for node in route:
            capacity += graph.getDemandMatrix(node[0],node[1]) 
        if capacity > graph.capacity:
            return False
    return True


def s_format(s):
    s_print = []
    for p in s:
        s_print.append(0)
        s_print.extend(p)
        s_print.append(0)
    return s_print

class vertex():
    def __init__(self,id):
        self.id = id
        self.visited = False
    
class edge():
    def __init__(self,start,end,cost,demand):
        self.start = int(start)
        self.end = int(end)
        self.cost = int(cost)
        self.demand = int(demand)
        self.isTask = True if self.demand != 0 else False
        self.visited = False


class graph():
    def __init__(self, Vertices, Depot, Tasks, Non_tasks, Vehicles, Capacity, Total_cost):
        self.vertices = int(Vertices) # the number of vertices 
        self.depot = Depot # the depot node(vertex)
        self.tasks = int(Tasks) # the number of tasks(required edges)
        self.tasks_list = []
        self.non_tasks = int(Non_tasks)  # the number of non-required edges
        self.vehicles = int(Vehicles) #  the number of vehicles
        self.capacity = int(Capacity)  # the capacity of each vehicle
        self.total_cost = int(Total_cost)  # the total cost of all tasks
        
        self.__edges = []
        self.__vertex = []

        # demand matrix
        self.__matrix = np.zeros([self.vertices+1,self.vertices+1]) 
        self.__matrix[self.__matrix == 0] = -1
        # -1 is no edge, others are edges with their demand

        # original cost matrix
        self.__costs = np.zeros([self.vertices+1, self.vertices+1])
        self.__costs[self.__costs == 0] = -1
        # -1 is no edge, others are the cost of their edge. 

        # distance matrix
        self.__distances = np.zeros([self.vertices+1, self.vertices+1])
        self.__distances[self.__distances == 0] = float("inf")
        for i in range(self.vertices+1):
            self.__distances[i,i] = 0
        # The shortest distance between every 2 nodes, inf for no edge between these 2 nodes.

        self.free = [] # free list
        pass
    
    def addEdge(self,edge):
        self.__edges.append(edge)
        self.__matrix[edge.start,edge.end] = self.__matrix[edge.end,edge.start] = edge.demand
        if edge.demand != 0:
            self.tasks_list.append(edge)
        self.free.append(edge)
        self.__distances[edge.start,edge.end] = self.__distances[edge.end,edge.start] = edge.cost
        self.__costs[edge.start,edge.end] = self.__costs[edge.end,edge.start] = edge.cost
        pass

    def getEdges(self):
        return copy.deepcopy(self.__edges)

    def setDistanceMatrix(self):
        for i in range(self.vertices): # i+1 is start node
            self.dijkstra(self.getDemandMatrix,i+1)
        pass

    def updateDistanceMatrix(self,start,goal,value):
        self.__distances[start,goal]  = value
        pass

    def getDistanceMatrix(self):
        return copy.deepcopy(self.__distances)

    def getCostMatrix(self):
        return copy.deepcopy(self.__costs)

    def getNeighbor(self,node):
        result = np.where(self.__matrix[node]!=-1)
        result = list(result[0])
        return result


    def addVertex(self,vertex):
        self.__vertex.append(vertex)

    def getVertex(self):
        return copy.deepcopy(self.__vertex)
    
    def getDemandMatrix(self):
        return copy.deepcopy(self.__matrix)

    def dijkstra(self,graph,start):
        heap = [] # the elements are (node,distance)
        visited = set()
        parent = {} # {node:its parent}
        
        visited.add(start)
        for node in self.getNeighbor(start):
            parent[node] = start
            heapq.heappush(heap,(self.getDistanceMatrix()[start,node],node))


        while len(heap):
            curr = heapq.heappop(heap)
            if curr[1] not in visited:
                visited.add(curr[1])
                for neighbor in self.getNeighbor(curr[1]):
                    if neighbor not in visited:
                        newDist = curr[0] + self.getDistanceMatrix()[curr[1],neighbor]
                        # print(start, " to ", neighbor, " new ", newDist, " old ",self.getDistanceMatrix()[start][neighbor])
                        if newDist < self.getDistanceMatrix()[start][neighbor]:
                            # print(start," to ", neighbor," update to ", newDist)
                            self.updateDistanceMatrix(start,neighbor,newDist)
                            parent[neighbor] = curr[1]
                            heapq.heappush(heap,(self.getDistanceMatrix()[start, neighbor],neighbor))
        # print(parent)

main()
