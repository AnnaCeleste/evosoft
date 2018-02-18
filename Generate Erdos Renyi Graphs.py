"""
Generate Erdos Renyi Graphs
Anna Hughes Hoge
February 6th, 2018
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

n = 50
k = 3
#degree = 5
#graph = nx.erdos_renyi_graph(n, degree/n)
#plt.subplot(121)
#nx.draw_networkx(graph, with_labels=True, font_weight='bold')

#write to file
for i in np.arange(0, 5.5, 0.5):
    for j in range(3):
        graph = nx.erdos_renyi_graph(n, i/n)
        filename = "ERGraph_" + str(i) + "_" + str(j) + ".txt"
        file = open(filename, "w")
        file.write(str(k) + "\n")
        for edge in graph.edges():
            file.write(str(edge[0]) + " " + str(edge[1]) + "\n")
        file.close()
