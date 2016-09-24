import GeneticAlgorithm as GA
import random

#def myFitness():
    #print("Hello world from myFitness!")

goal = 190

correctGraph = []

def PickRandomGene():
    #print("Inside pick random gene!")
    gene = int(random.uniform(0, 100))
    #print("returning: " + str(gene))
    return gene

def GenerateRandomChromosome():
    return [PickRandomGene(), PickRandomGene(), PickRandomGene(), PickRandomGene()]

def Fitness(chromosome):
    total = 0
    for gene in chromosome:
        total += int(gene)

    if total == goal: return 100000000
    #print("total: " + str(total) + " goal: " + str(goal) + " difference: " + str(goal - total))
    #return float(1/float(abs(goal - total)))
    return (400 - abs(goal - total))**2

    

alg = GA.GeneticAlgorithm(Fitness, PickRandomGene, GenerateRandomChromosome)
#alg.CrossoverProbability = 0.0
#alg.MutationProbability = 0.02
alg.PopulationSize = 5000
alg.SetElitismSelection(2500)
alg.FillRemaining() # initial population
alg.EvaluatePopulation()


def printPopulation(generation):
    index = 0
    print("----------------------------------------")
    accurate = 0
    for entry in alg.SortedPopulation:
        #if index >= 20: return
        total = 0
        chromosome = entry["chromosome"]
        extraString = ""
        for gene in chromosome: total += int(gene)
        if total == goal: extraString = "         ===== GOAL!!!! ====="; accurate += 1
        if index <= 20: print("GENERATION " + str(generation) + " " + str(entry) + "\t :: \t" + str(total) + extraString)
        index += 1

    print("GENERATION STATS: correct: " + str(accurate) + "")
    correctGraph.append(accurate)
        


for i in range(0, 200):
    alg.GenerateNextPopulation()
    alg.EvaluatePopulation()
    printPopulation(i)
    #raw_input()

#print(alg.SortedPopulation)

print(correctGraph)
