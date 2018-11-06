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