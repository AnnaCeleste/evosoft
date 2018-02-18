""" 
Graph Coloring Balanced Coloring
Anna Hughes Hoge
February 6th, 2018
"""
#variables
seed = 22
#Graph1.g, Graph2.g, Graph3.g, Graph5.g, Graph6.g
filename = "Graph5.g"
num_generations = 1
CXPB = 0.6 #the probability with which 2 individials are crossed


#imports
import random
import networkx as nx
import matplotlib.pyplot as plt
from deap import base
from deap import creator
from deap import tools
from collections import Counter


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

num_nodes = graph.number_of_nodes()
int_node_list = [int(node) for node in graph.nodes()]
last_node = max(int_node_list)
num_edges = graph.number_of_edges()


#plot graph
plt.subplot(121)
nx.draw_networkx(graph, with_labels=True, font_weight='bold')


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
    toolbox.attr_color, last_node)
#the population is a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


#FITNESS FUNCTION DEFINITION
#the fitness function to be maximized
def fitness_eval(individual):
    """Returns balanced coloring fitness function value, normalized to [0, 1]."""
    sum = 0
    for edge in graph.edges():
        node1 = int(edge[0])
        node2 = int(edge[1])
        color_node1 = individual[node1 - 1]
        color_node2 = individual[node2 - 1]
        if color_node1 != color_node2:
            sum += 1
    result = sum / num_edges
    
    color_occurances = Counter(individual)
    product = 1
    for i in range(k):
        product = product * color_occurances[i+1] / last_node
    result = result * product
    
    result = result * (k**k)
    return (result, )


#OPERATOR REGISTRATION
#registering the fitness function
toolbox.register("evaluate", fitness_eval)

#registering the 2-point crossover operator
toolbox.register("mate", tools.cxTwoPoint)

#registering the mutation operator with P of gene mutation = 1/num_nodes
toolbox.register("mutate", tools.mutUniformInt, low = 1, up = k,
                 indpb = 1/last_node)

#registering selection operator for breeding next generation
#each individual of current generation is replaced by fittest of 2 drawn
#  randomly from current generation
toolbox.register("select", tools.selTournament, tournsize = 2)


#MAIN

random.seed(seed)

#create initial population of 2*num_nodes individuals
pop = toolbox.population(n = 2*last_node)
print("Start of evolution: %s, %i nodes, %i edges, %i colors"
      % (filename, last_node, num_edges, k))

#evaluate entire population
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
#print("  Evaluated %i individuals" % len(pop))

#extracting fitnesses of individuals
fits = [ind.fitness.values[0] for ind in pop]

#to keep track of the number of generations
g = 0

max_fit_achieved = 0
best_ind_found= []
gen_found = 0
all_max_fits = []


#begin evolving
while max(fits) < 1 and g < num_generations:
    #new generation
    g = g + 1
    #print("-- Generation %i --" % g)
    
    #tournament selection of offspring
    offspring = toolbox.select(pop, len(pop))
    #clone selected individuals
    offspring = list(map(toolbox.clone, offspring))

    #apply crossover to offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
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
    #print("  Evaluated %i individuals" % len(invalid_ind))
    
    #replace population by offspring
    pop[:] = offspring
    
    #gather fitnesses and print statistics
    fits = [ind.fitness.values[0] for ind in pop]
    #length = len(pop)
    #mean = sum(fits) / length
    #sum2 = sum(x*x for x in fits)
    #std = abs(sum2 / length - mean**2)**0.5
    
    #print("  Min %s" % min(fits))
    #print("  Max %s" % max(fits))
    print("  Max %s, generation %i" % (max(fits), g))
    #print("  Avg %s" % mean)
    #print("  Std %s" % std)
    
    rounded_max = round(max(fits), 6)
    all_max_fits.append(rounded_max)

    if rounded_max > max_fit_achieved:
        max_fit_achieved = rounded_max
        best_ind_found = tools.selBest(pop, 1)[0]
        gen_found = g

print("-- End of evolution --")

def color_fitness_eval(individual):
    """Returns ???"""
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

valid = color_fitness_eval(best_ind_found) == 1.0

print("First best ind was %s, with %s fitness, at gen %i, valid is %s" % (best_ind_found, max_fit_achieved, gen_found, valid))


#best_ind = tools.selBest(pop, 1)[0]
#print("Best individual is %s, with %s fitness" % (best_ind, best_ind.fitness.values))
