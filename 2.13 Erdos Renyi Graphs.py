# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 15:52:04 2018

@author: bob
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

#do evolution to find max fitness

#plot degree of different files against max fitness achieved for that file

#for each value of d with a valid coloring, do the neutrality thing