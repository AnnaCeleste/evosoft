"""
Neutral Colorings
Anna Hughes Hoge
February 13th, 2018
"""
#Graph1.g, Graph2.g, Graph3.g, Graph4.txt, Graph5.g, Graph6.g
filename = "Graph6.g"

#imports
import random
import networkx as nx
import matplotlib.pyplot as plt
from deap import base
from deap import creator
from deap import tools
import numpy as np

#get graph
with open(filename, "r") as file:
    #first line of input file supplies k, the number of colors to be used
    k = int(file.readline())
    edges = []
    #other lines in file give edges of graphs
    for line in file.readlines():
        line = line.rstrip("\n")
        edges.append(tuple(line.split(" ")))
graph = nx.Graph()
graph.add_edges_from(edges)

num_edges = graph.number_of_edges()



#graph3 is 5

#graph data in the form (valid coloring, k)
graph1_data = ([2, 1, 4, 4, 1, 3, 1, 3, 3, 1, 2], 4)
graph2_data = ([4, 2, 4, 1, 3, 3, 1, 2, 3, 3, 2, 4, 2, 4, 2, 4, 2, 3, 1, 2, 1, 
                2, 1, 1, 4, 1, 1, 3, 2, 3, 2, 3, 3, 3, 2, 2, 1], 4)
graph5_data = ([8, 4, 4, 9, 7, 1, 8, 4, 2, 10, 9, 8, 2, 7, 3, 8, 4, 9, 4, 6, 3,
                8, 6, 9, 6, 2, 3, 9, 6, 4, 7, 4, 8, 6, 4, 10, 5, 9, 2, 9, 3, 8,
                3, 8, 4, 8, 5, 5, 9, 3, 5, 5, 10, 10, 2, 8, 6, 7, 10, 7, 2, 6,
                7, 8, 8, 1, 4, 7, 10, 7, 10, 10, 1, 9, 2, 5, 8, 7, 5, 8], 10)
graph6_data = ([4, 5, 2, 3, 1, 3, 1, 4, 5, 2, 5, 2, 3, 1, 4, 1, 4, 5, 2, 3, 2,
                3, 1, 4, 5], 5)
er1 = ([3, 3, 1, 1, 3, 3, 3, 2, 2, 3, 2, 1, 2, 2, 3, 1, 2, 3, 2, 3, 2, 1, 3, 1, 2, 2, 2, 1, 2, 3, 3, 3, 1, 3, 1, 1, 1, 2, 2, 1, 1, 3, 3, 1, 1, 3, 2, 3, 1], 3)
er2 = ([1, 1, 1, 2, 2, 3, 2, 3, 1, 1, 2, 3, 1, 1, 3, 1, 2, 1, 1, 1, 2, 2, 2, 1, 3, 1, 1, 3, 2, 1, 1, 1, 3, 3, 2, 1, 1, 3, 2, 3, 3, 3, 2, 2, 1, 1, 1], 3)
er3 = ([3, 1, 3, 1, 3, 2, 1, 3, 1, 3, 1, 1, 2, 2, 2, 2, 2, 3, 3, 1, 3, 1, 1, 2, 2, 1, 2, 1, 3, 1, 3, 2, 3, 2, 1, 3, 2, 1, 2, 1, 1, 3, 3, 3, 2, 2, 2, 3, 1], 3)
er4 = ([1, 1, 3, 3, 1, 2, 1, 2, 2, 2, 1, 1, 2, 3, 2, 3, 1, 3, 1, 3, 2, 1, 3, 3, 1, 3, 3, 1, 3, 2, 1, 3, 1, 2, 3, 3, 2, 1, 3, 2, 2, 2, 2, 1, 1, 3, 3, 3, 3], 3)
er5 = ([3, 1, 1, 1, 2, 3, 2, 3, 2, 1, 3, 1, 2, 2, 2, 2, 3, 1, 2, 2, 1, 3, 3, 3, 3, 1, 3, 3, 3, 1, 3, 3, 2, 1, 3, 1, 1, 2, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 2], 3)
er6 = ([1, 3, 2, 1, 3, 1, 3, 1, 2, 2, 1, 3, 2, 2, 3, 1, 1, 2, 3, 2, 3, 3, 2, 1, 1, 3, 1, 1, 2, 1, 3, 1, 3, 1, 2, 1, 3, 3, 2, 2, 1, 3, 2, 1, 3, 3, 1, 3, 2], 3)
er7 = ([2, 2, 1, 1, 3, 2, 3, 1, 2, 3, 2, 2, 3, 1, 1, 3, 3, 2, 3, 1, 2, 2, 3, 2, 1, 3, 2, 3, 3, 1, 2, 2, 2, 2, 1, 3, 3, 2, 2, 3, 2, 1, 1, 3, 3, 2, 2, 1, 1], 3)
er8 = ([2, 2, 1, 1, 3, 2, 2, 3, 2, 1, 1, 2, 1, 3, 2, 3, 2, 1, 2, 3, 3, 1, 2, 3, 3, 1, 1, 1, 1, 3, 2, 1, 1, 1, 2, 2, 1, 3, 3, 2, 2, 1, 3, 2, 2, 3, 1, 1, 2], 3)

#pick a graph
graph_data = graph6_data

coloring = graph_data[0]
k = graph_data[1]


def generate_one_step_colorings(coloring):
    step = []
    for i in range(len(coloring)):
        current_color = coloring[i]
        for j in range(1, k+1):
            if current_color != j:
                new_coloring = coloring.copy()
                new_coloring[i] = j
                step.append(new_coloring)
    return step

def fitness_eval(individual):
    """Returns the fraction of edges that do not share the same color,
    divided by the total number of edges (as the first element of a tuple.)"""
    sum = 0
    for edge in graph.edges():
        node1 = int(edge[0])
        node2 = int(edge[1])
        color_node1 = individual[node1 - 1]
        color_node2 = individual[node2 - 1]
        if color_node1 != color_node2:
            sum += 1
    result = sum / num_edges
    return result


step_colorings = generate_one_step_colorings(coloring)

valid_count = 0

for step_c in step_colorings:
    fitness = fitness_eval(step_c)
    if fitness == 1.0:
        valid_count += 1
neutrality = valid_count/len(step_colorings)
print(neutrality)


def er_neutrality_graph():
    d = np.arange(0.5, 4.5, 0.5)
    neutrality = [0.8469387755102041, 0.6063829787234043, 0.46938775510204084,
                  0.2755102040816326, 0.23469387755102042, 0.23469387755102042,
                  0.14285714285714285, 0.09183673469387756]
    plt.scatter(d, neutrality)
    plt.ylabel("1-Step Neutrality", size = 12)
    plt.xlabel("Degree of Erdos-Renyi Graph", size = 12)
    plt.title("The Effect of Graph Degree on Neutrality of Coloring", size = 14)

er_neutrality_graph()