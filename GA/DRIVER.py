import GeneticAlgorithm as GA
import random

#def myFitness():
    #print("Hello world from myFitness!")

goal = 69

def PickRandomGene():
    #print("Inside pick random gene!")
    gene = int(random.uniform(0, 50))
    #print("returning: " + str(gene))
    return gene

def GenerateRandomChromosome():
    return [PickRandomGene(), PickRandomGene(), PickRandomGene(), PickRandomGene()]

def Fitness(chromosome):
    total = 0
    for gene in chromosome:
        total += int(gene)

    if total == goal: return 100000000
    return 1/(abs(goal - total))

    

alg = GA.GeneticAlgorithm(Fitness, PickRandomGene, GenerateRandomChromosome)
alg.PopulationSize = 50
alg.SetElitismSelection(25)
alg.FillRemaining() # initial population
alg.EvaluatePopulation()


for i in range(0, 10):
    alg.GenerateNextPopulation()
    alg.EvaluatePopulation()

print(alg.SortedPopulation)
