# CARP
# The definition of CARP
CARP - Capacitated Arc Routing Problem

Consider an undirected connected graph 𝐺 = (𝑉, 𝐸), with a vertex set 𝑉 and an edge set 𝐸 and a set of required edges (tasks) 𝑇 ⊆ 𝐸. 
A fleet of identical vehicles, each of capacity 𝑄, is based at a designated depot vertex 𝑣0 ∈𝑉. Each edge 𝑒∈𝐸 incurs a cost 𝑐(𝑒)whenever a vehicle travels over it or serves it (if it is a task). Each required edge (task) 𝜏 ∈ 𝑇 has a demand 𝑑(𝜏) > 0 associated with it.
The objective of CARP is to determine a set of routes for the vehicle to serve all tasks with minimal costs while satisfying:
    a) Each route must start and end at 𝑣0; 
    b) The total demand serviced on each route must not exceed 𝑄;
    c) Each task must be served exactly once (but the corresponding edge can be traversed more than once)

一个车队从一个停车场出发，对已知需求的若干位于arc上的客户进行服务。求在满足车辆capacity及各种约束下使服务成本最低的车辆行驶路线。

# Common heuristic method to solve CARP
- 模拟退火算法
- 禁忌搜索算法
- 改进的遗传算法
- tabu-scatter算法

# Input
- the graph G(V,E)
- the cost c(e), and the demand d(e) for each e
- the tasks set T
- v0
- capacity Q


# Steps
Step1: calculate the shortest distance between the depot to every other node. -> 2D-matrix `distances`
Step2: use Path-Scanning method to get a feasible solution
Step3(if have enough time): use the feasible solution as the initial population and use the genetic algorithm to iteration to get a better solution

# Usage
Use the command `python CARP_solver.py < CARP instance file > -t <termination> -s <random seed>` in terminal. 
output: 
Print two lines. Each of them, according to its first char, must belong to one of the categories described below. Lines that do not start with one of the patterns below will be considered a comment and hence ignored.
Solution line begins with a lower case “s” followed by a space (ASCII code 32). Only one such line is allowed and it is mandatory.
Quality line begins with a lower case “q” followed by a space (ASCII code 32). Only one such line is allowed and it is mandatory.

e.g.
```
s 0,(1,2),(2,4),(4,1),0,0,(4,3),(3,1),0
q 40
```

