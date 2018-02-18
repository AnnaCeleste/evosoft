"""
Graph Coloring Pichsurs
Anna Hughes Hoge
FEBRUARY 11th, 2018!!!  HAPPY 22nd BIRFDAY, NABOO!!!!!!!!!!  : )  : )  : )  : )  : )
"""
#variables
seed = 22
#Graph1.g, Graph2.g, Graph3.g, Graph6.g
filename = "Graph6.g"
num_generations = 1000
CXPB = 0.6 #the probability with which 2 individials are crossed


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

num_nodes = graph.number_of_nodes()
num_edges = graph.number_of_edges()


#plot graph
#plt.subplot(121)
#nx.draw_networkx(graph, with_labels=True, font_weight='bold')


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


#MAIN
all_max_fits = []
all_mean_fits = []
all_min_fits = []

for i in range(20):
    seed = i
    max_fits = []
    mean_fits = []
    min_fits = []
    
    random.seed(seed)

    #create initial population of 2*num_nodes individuals
    pop = toolbox.population(n = 2*num_nodes)
    print("Start of evolution: %s, %i nodes, %i edges, %i colors"
          % (filename, num_nodes, num_edges, k))
    
    #evaluate entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    #print("  Evaluated %i individuals" % len(pop))

    #extracting fitnesses of individuals
    fits = [ind.fitness.values[0] for ind in pop]

    #to keep track of the number of generations
    g = 0
    
    #begin evolving
    while g < num_generations:
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
        length = len(pop)
        mean = sum(fits) / length
        #sum2 = sum(x*x for x in fits)
        #std = abs(sum2 / length - mean**2)**0.5
        
        #print("  Min %s" % min(fits))
        #print("  Max %s" % max(fits))
        #print("  Avg %s, generation %i" % (mean, g))
        #print("  Std %s" % std)
        max_fits.append(max(fits))
        mean_fits.append(mean)
        min_fits.append(min(fits))
    #print("-- End of evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, with %s fitness, at gen %i" % (best_ind, best_ind.fitness.values, g))
    all_max_fits.append(max_fits)
    all_mean_fits.append(mean_fits)
    all_min_fits.append(min_fits)

print("done")
av_max_fits = np.mean(all_max_fits, axis = 0)
av_mean_fits = np.mean(all_mean_fits, axis = 0)
av_min_fits = np.mean(all_min_fits, axis = 0)

plt.plot(av_max_fits, label = "Highest Fitness")
plt.plot(av_mean_fits, label = "Mean Fitness")
plt.plot(av_min_fits, label = "Min Fitness")
plt.legend()
plt.ylabel("Fitness", size = 12)
plt.xlabel("Generation", size = 12)
plt.title("Average Fitness Over Generations, 20 Trials", size = 14)