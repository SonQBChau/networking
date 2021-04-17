#############################################
# Name: Son Chau (sonchau@my.unt.edu)
# Course: CSE 5580 Networking Spring 2021
# Date: 04/22/2021
# Description: implement the OSPF link-state (LS)
# algorithm for a given set of nodes identified
# by a lower-case letter (a – z). The output of
# the program will be the shortest path cost and
# path taken for each node, when given a source node.
#############################################

from pathlib import Path

###########################################
# FIND THE INDEX WITH THE MINIMUM DISTANCE
###########################################
def minDistance(dist,queue):
    minimum = float("Inf")
    min_index = -1
    for i in range(len(dist)):
        if dist[i] < minimum and i in queue:
            minimum = dist[i]
            min_index = i
    return min_index

##########################################################
# BACKTRACK FROM END-NODE TO START-NODE TO GET TRAVEL PATH 
##########################################################
def getPath(parent, j, result=''):
    result += str(j)
    if parent[j] == -1 : 
        return result
    return getPath(parent, parent[j], result=result)

#################################
# PRINT PATH COST AND ROUTE TAKEN
#################################
def printSolution(dist, parent, representation_node, source_router):
    representation_ascii = ord(representation_node)
    for i in range(0, len(dist)):
        dest_node = chr(representation_ascii + i)
        reserve_path = ''
        print('{} ==> {}:'.format(source_router, dest_node))
        print('path cost: {}'.format(dist[i]))
        path = getPath(parent,i)
        # since path is in reversed order, we need to switch it back
        for node in reversed(path):
            node_name = chr(int(node) + representation_ascii)
            reserve_path += node_name + ' --> '
        reserve_path = reserve_path[:-5] # remove extra string at the end
        print('path taken: {}'.format(reserve_path))

#########################################
# RUN DIJKSTRA'S SHORTEST PATH ALGORITHM
#########################################
def runLinkState(graph, src):
        row = len(graph)
        col = len(graph[0])
        dist = [float("Inf")] * row
        parent = [-1] * row
        dist[src] = 0
        queue = []
        for i in range(row):
            queue.append(i)
        while queue:
            u = minDistance(dist,queue)  
            queue.remove(u)
            for i in range(col):
                if graph[u][i] and i in queue:
                    if (dist[u] + graph[u][i] < dist[i]) and graph[u][i] > 0:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u
        return (dist,parent)

#######################################
# READ FILE INPUT AND RETURN A 2D ARRAY
#######################################
def readFile(name):
    matrix = []
    script_location = Path(__file__).absolute().parent
    file_location = script_location / name
    f = open(file_location, "r")
    for line in f.readlines():
            matrix.append([int(d) for d in line.split(' ')])
    f.close()
    return matrix


def main():
    print('OSPF Link-State (LS) Routing:')
    print(('-' * 29))
    # router_num = int(input("Enter the number of routers: "))
    # input_name = input("Enter filename with cost matrix values: ")
    # representation_node = input("Enter character representation of first node: ")
    # source_router = input("Enter the source router: ")
    #need error checking

    router_num = 0
    input_name = 'text.txt'
    representation_node = 'u'
    source_router = 'v'
    source_index = ord(source_router) - ord(representation_node)

    matrix = readFile(input_name)
    dist, parent = runLinkState(matrix,source_index)
    printSolution(dist,parent, representation_node, source_router)


if __name__ == "__main__":
    main()


