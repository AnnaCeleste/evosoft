# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 19:16:01 2018

@author: bob
"""
#variables
SEED = 22
CXPROB = 0.6
NUM_GENERATIONS = 1000

#imports
import random
import networkx as nx
import matplotlib.pyplot as plt
from deap import base
from deap import creator
from deap import tools


def get_problem(filename):
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
    
    #to get the total number of nodes, connected or unconnected
    int_node_list = [int(node) for node in graph.nodes()]
    num_nodes = max(int_node_list)
    num_edges = graph.number_of_edges()
    
    return graph, k, num_nodes, num_edges


def plot_graph(graph):
    plt.subplot(121)
    nx.draw_networkx(graph, with_labels=True, font_weight='bold')


#FITNESS FUNCTION DEFINITION
#the fitness function to be maximized
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
    return (result, )


def set_up(k, num_nodes):
    #ALGORITHM SET-UP
    #a single fitness function (with weight 1) will be used
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    #individuals will be lists
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    
    #ATTRIBUTE GENERATION
    #a color attribute/gene is a random integer between 1 and k
    toolbox.register("attr_color", random.randint, 1, k)
    
    #STRUCTURE INITIALIZERS
    #an individual consists of num_nodes number of color attributes
    toolbox.register("individual", tools.initRepeat, creator.Individual, 
        toolbox.attr_color, num_nodes)
    #the population is a list of individuals
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    #OPERATOR REGISTRATION
    #registering the fitness function
    toolbox.register("evaluate", fitness_eval)
    
    #registering the 2-point crossover operator
    toolbox.register("mate", tools.cxTwoPoint)
    
    #registering the mutation operator with P of gene mutation = 1/num_nodes
    toolbox.register("mutate", tools.mutUniformInt, low = 1, up = k,
                     indpb = 1/num_nodes)
    
    #registering selection operator for breeding next generation
    #each individual of current generation is replaced by fittest of 2 drawn
    #  randomly from current generation
    toolbox.register("select", tools.selTournament, tournsize = 2)
    return toolbox


def evolve(filename, num_nodes, num_edges, k, num_generations, cxprob, seed,
           toolbox):
    random.seed(seed)
    #create initial population of 2*num_nodes individuals
    pop = toolbox.population(n = 2*num_nodes)
    print("Start of evolution: %s, %i nodes, %i edges, %i colors"
          % (filename, num_nodes, num_edges, k))
    
    #evaluate entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print("  Evaluated %i individuals" % len(pop))
    
    #extracting fitnesses of individuals
    fits = [ind.fitness.values[0] for ind in pop]
    
    #to keep track of the number of generations
    g = 0
    
    #begin evolving
    while max(fits) < 1 and g < num_generations:
        #new generation
        g = g + 1        
        #tournament selection of offspring
        offspring = toolbox.select(pop, len(pop))
        #clone selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
        #apply crossover to offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxprob:
                toolbox.mate(child1, child2)
                #fitness values of the children must be recalculated later
                del child1.fitness.values
                del child2.fitness.values
    
        #mutate offspring
        for mutant in offspring:
            toolbox.mutate(mutant)
            del mutant.fitness.values
    
        #evaluate individuals with invalid fitness values
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        #replace population by offspring
        pop[:] = offspring
        
        #gather fitnesses and print statistics
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        #sum2 = sum(x*x for x in fits)
        #std = abs(sum2 / length - mean**2)**0.5
        
        #print("  Min %s" % min(fits))
        #print("  Max %s" % max(fits))
        print("  Avg %s, generation %i" % (mean, g))
        #print("  Std %s" % std)
    
    print("-- End of evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, with %s fitness" % (best_ind,
                                                      best_ind.fitness.values))
    return best_ind, best_ind.fitness.values


if __name__ == "__main__":
    filename = input("What file is your graph contained in?  ")
    graph, k, num_nodes, num_edges = get_problem(filename)
    #plot_graph(graph)
    toolbox = set_up(k, num_nodes)
    best_ind, best_ind_fitness = evolve(filename, num_nodes, num_edges, k, 
                                        NUM_GENERATIONS, CXPROB, SEED, toolbox)