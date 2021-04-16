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
import sys
from pathlib import Path

from collections import defaultdict
  
#Class to represent a graph
class Graph:
  
    # A utility function to find the 
    # vertex with minimum dist value, from
    # the set of vertices still in queue
    def minDistance(self,dist,queue):
        # Initialize min value and min_index as -1
        minimum = float("Inf")
        min_index = -1
          
        # from the dist array,pick one which
        # has min value and is till in queue
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index
  
  
    # Function to print shortest path
    # from source to j
    # using parent array
    def printPath(self, parent, j):
        src = ord('u')
        node = chr(src+j)
        #Base Case : If j is source
        if parent[j] == -1 : 
            print (node, end=', '),
            return
        self.printPath(parent , parent[j])
        print (node, end=', '),

      # Function to print shortest path
    # from source to j
    # using parent array 
    def getPath(self, parent, j, result=''):
        src = ord('u')
        node = chr(src+j)
        result += node
        #Base Case : If j is source
        if parent[j] == -1 : 
            return result
        return self.getPath(parent, parent[j], result=result)
 
  
    # A utility function to print
    # the constructed distance
    # array
    def printSolution(self, dist, parent):
        src = ord('u')
        cha = chr(src)
        for i in range(0, len(dist)):
            node = chr(src+i)
            reserve_path = ''
            print('{} ==> {}:'.format(cha, node))
            print('path cost: {}'.format(dist[i]))
            path = self.getPath(parent,i)
            
            # Iterate over the string
            for element in reversed(path):
                reserve_path += element + ' --> '
            reserve_path = reserve_path[:-5]
            print('path taken: {}'.format(reserve_path))
            # self.printPath(parent,i)
  
  
    '''Function that implements Dijkstra's single source shortest path
    algorithm for a graph represented using adjacency matrix
    representation'''
    def dijkstra(self, graph, src):
  
        row = len(graph)
        col = len(graph[0])
  
        # The output array. dist[i] will hold
        # the shortest distance from src to i
        # Initialize all distances as INFINITE 
        dist = [float("Inf")] * row
  
        #Parent array to store 
        # shortest path tree
        parent = [-1] * row
  
        # Distance of source vertex 
        # from itself is always 0
        dist[src] = 0
      
        # Add all vertices in queue
        queue = []
        for i in range(row):
            queue.append(i)
              
        #Find shortest path for all vertices
        while queue:
  
            # Pick the minimum dist vertex 
            # from the set of vertices
            # still in queue
            u = self.minDistance(dist,queue) 
  
            # remove min element     
            queue.remove(u)
  
            # Update dist value and parent 
            # index of the adjacent vertices of
            # the picked vertex. Consider only 
            # those vertices which are still in
            # queue
            for i in range(col):
                '''Update dist[i] only if it is in queue, there is
                an edge from u to i, and total weight of path from
                src to i through u is smaller than current value of
                dist[i]'''
                if graph[u][i] and i in queue:
                    if (dist[u] + graph[u][i] < dist[i]) and graph[u][i] > 0:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u
  
  
        # print the constructed distance array
        self.printSolution(dist,parent)
  


def main():
    # no_of_router = int(input("Enter the number of routers: "))
    # matrix_name = input("Enter filename with cost matrix values: ")
    # first_node_char = input("Enter character representation of first node: ")
    # source_router = input("Enter the source router: ")
    # print(f'You entered {value}')

    array2D = []

    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'text.txt'
    f = open(file_location, "r")
    for line in f.readlines():
            # array2D.append(line.split(' '))
            array2D.append([int(d) for d in line.split(' ')])
    print(array2D)
    f.close()

    # Driver program
    g = Graph()
    graph = array2D
    # graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
    #     [4, 0, 8, 0, 0, 0, 0, 11, 0],
    #     [0, 8, 0, 7, 0, 4, 0, 0, 2],
    #     [0, 0, 7, 0, 9, 14, 0, 0, 0],
    #     [0, 0, 0, 9, 0, 10, 0, 0, 0],
    #     [0, 0, 4, 14, 10, 0, 2, 0, 0],
    #     [0, 0, 0, 0, 0, 2, 0, 1, 6],
    #     [8, 11, 0, 0, 0, 0, 1, 0, 7],
    #     [0, 0, 2, 0, 0, 0, 6, 7, 0]
    #     ]

#     graph =[[ 0, 2, 5, 1, 0, 0],
# [2, 0, 3, 2, 0, 0],
# [5, 3, 0, 3, 1, 5],
# [1, 2, 3, 0, 1, 0],
# [0, 0, 1, 1, 0, 2],
# [0, 0, 5, 0, 2, 0]]

    g.dijkstra(graph,0)


if __name__ == "__main__":
    main()


