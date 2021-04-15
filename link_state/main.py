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

class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def printSolution(self, dist):
        print("Vertex tDistance from Source")
        for node in range(self.V):
            print(node, "t", dist[node])

    # A utility function to find the vertex with
    # minimum distance value, from the set of vertices
    # not yet included in shortest path tree
    def minDistance(self, dist, sptSet):
        # Initilaize minimum distance for next node
        min = sys.maxsize

        # Search not nearest vertex not in the
        # shortest path tree
        for v in range(self.V):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
        return min_index

    # Funtion that implements Dijkstra's single source
    # shortest path algorithm for a graph represented
    # using adjacency matrix representation
    def dijkstra(self, src):

        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
        path_taken = [''] * self.V

        for cout in range(self.V):

            # Pick the minimum distance vertex from
            # the set of vertices not yet processed.
            # u is always equal to src in first iteration
            u = self.minDistance(dist, sptSet)

            # Put the minimum distance vertex in the
            # shotest path tree
            sptSet[u] = True

            # Update dist value of the adjacent vertices
            # of the picked vertex only if the current
            # distance is greater than new distance and
            # the vertex in not in the shotest path tree
            for v in range(self.V):
                if (
                    self.graph[u][v] > 0 and
                    sptSet[v] == False and
                    dist[v] > dist[u] + self.graph[u][v]
                    ):
                    dist[v] = dist[u] + self.graph[u][v]
                    path_taken[v] += str(u)
            print('======')
            print(dist)
            print(path_taken)
        self.printSolution(dist)


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
    g = Graph(6)
    g.graph = array2D

    g.dijkstra(0)


if __name__ == "__main__":
    main()


