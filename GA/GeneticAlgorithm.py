import random

class GeneticAlgorithm:


    # TODO: save last generation
    # TODO: minimize/maximze option?

    SelectionType = "StochasticUniversal" # "StochasticUniversal", "FitnessProportionate", "Tournament", "RewardBased", "Truncation", "Elitism"
    CrossoverType = "Single" # "Single","Double", "CutSplice", "Uniform"
    CrossoverProbability = 0.2
    MutationProbability = 0.001


    # Selection type specific variables
    ElitismSize = 500

    

    PopulationSize = 1000

    #EncodingChart = {} # handled in a wrapper, not here?
    #DecodingChart = {} # handled in a wrapper, not here? #NOTE: there should be functions to handle encoding/decoding?

    #CurrentPopulation = [ ["0100101",0.0] ] # chromosome and fitness
    #SortedPopulation = [] # use this as a buffer while evaluating population fitness, then set Current to this
    #NextPopulation = []

    
    # NOTE: population should consist of an array of dictionaries, where each
    # dictionary contains a chromosome (array of genes) and a float fitness


    #CurrentPopulation = [ { "chromosome":['s', 'a', 'm', 'p', 'l', 'e'], "fitness":0.0 } ]
    CurrentPopulation = []
    SortedPopulation = [] # fitness sorted population list
    NextPopulation = [] # buffer to build up new population in?

    SelectedParents = []


    # GENERIC!!!!

    # ----------------------------------------------------------------------------
    #   SETTABLE FUNCTIONS
    # ----------------------------------------------------------------------------

    # should return array with genes
    def GenerateRandomChromosome(self):
        pass

    # should return some random gene
    def PickRandomGene(self): # potentially pass this in as a function?
        pass

    # Set by the wrapper. Should accept a chromosome, and should return a float fitness
    def Fitness(self, chromosome):
        print("Checking fitness...")
        return 0.0


    # runs the Fitness on every chromosome in CurrentPopulation and sets its fitness
    def EvaluatePopulation(self):
        self.SortedPopulation = []
        for chromosomeEntry in self.CurrentPopulation:
            chromosomeEntry["fitness"] = self.Fitness(chromosomeEntry["chromosome"])
            self.AddChromosomeEntryToSorted(chromosomeEntry)

        # all of population evaluated and sorted in SortedPopulation, TODO: do
        # we set current to sorted or just leave it?

    # call this as running evaluate population, and insert wherever this
    # new chromosome has a greater fitness then one at that location
    def AddChromosomeEntryToSorted(self, newChromosomeEntry):
        for i in range(0, len(self.SortedPopulation)):
            chromosomeEntry = self.SortedPopulation[i];
            if newChromosomeEntry["fitness"] >= chromosomeEntry["fitness"]:
                self.SortedPopulation.insert(i, newChromosomeEntry)
                return
            
        # if reached this point, list either empty, or lowest fitness score, so
        # store at end
        self.SortedPopulation.append(newChromosomeEntry)
    

    def GenerateNextPopulation(self):
        self.Selection()
        self.Crossover()       
        self.Mutate()
        self.CurrentPopulation = self.NextPopulation
        self.NextPopulation = []
        self.FillRemaining()

    def FillRemaining(self):
        while len(self.CurrentPopulation) < self.PopulationSize:
            self.CurrentPopulation.append({"chromosome":self.GenerateRandomChromosome(), "fitness":0.0})

    def Selection(self):
        if self.SelectionType == "Elitism":
            for i in range(0, self.ElitismSize):
                #print(" SELECTING " + str(self.SortedPopulation[i]))
                self.SelectedParents.append(self.SortedPopulation[i]["chromosome"])

    def Crossover(self):
        while len(self.SelectedParents) >= 1:
            index1 = len(self.SelectedParents) - 1
            index2 = len(self.SelectedParents) - 2
            #parent1 = self.SelectedParents[len(self.SelectedParents) - 1]
            #parent2 = self.SelectedParents[len(self.SelectedParents) - 2]
            parent1 = self.SelectedParents[index1]
            parent2 = self.SelectedParents[index2]

            #print("parent1: " + str(parent1) + " " + str(index1))
            #print("parent2: " + str(parent2) + " " + str(index2))
            
            crossoverRoll = random.random()

            child1 = []
            child2 = []
            
            if crossoverRoll >= self.CrossoverProbability:
                child1 = parent1
                child2 = parent2
            else:
                #print("CROSSING OVER")
                if self.CrossoverType == "Single":
                    # get two lengths, and get a random number that is less than
                    # either (minimum)
                    len1 = len(parent1)
                    len2 = len(parent2)
                    minlen = min(len1, len2)

                    crossPoint = int(random.uniform(0, minlen))

                    # carry out the crossover
                    child1 = parent1[0:crossPoint]
                    child1 += parent2[crossPoint:len2]
                    child2 = parent2[0:crossPoint]
                    child2 += parent1[crossPoint:len1]

            # remove parents and add children to new population
            del self.SelectedParents[len(self.SelectedParents) - 1]
            del self.SelectedParents[len(self.SelectedParents) - 1]
            self.NextPopulation.append({"chromosome":child1, "fitness":0.0})
            self.NextPopulation.append({"chromosome":child2, "fitness":0.0})

        #print("Next population: ")
        #for chromosome in self.NextPopulation:
            #print(str(chromosome))
        #print("REMAINING PARENTS: " + str(len(self.SelectedParents)))

    # randomly mutates entries in nextpopulation based on mutation probability 
    def Mutate(self):
        for chromosome in self.NextPopulation: # TODO: better name than chromosome here
            #print(str(chromosome))
            mutateRoll = random.random()

            if mutateRoll <= self.MutationProbability:
                #print("MUTATING")
                geneCount = len(chromosome["chromosome"])

                mutateGeneIndex = int(random.uniform(0, geneCount))
                newGene = self.PickRandomGene()
                #print(str(newGene))
                chromosome["chromosome"][mutateGeneIndex] = newGene
            
        pass


    #def SetTournamentSelection(self, tournamentSize=500):
    def SetElitismSelection(self, selectionSize=500):
        self.SelectionType = "Elitism"
        self.ElitismSize = selectionSize


    def RunGeneration(self):
        pass
        # generate population that doesn't exist
        #while len(CurrentPopulation) < self.PopulationSize:
            #CurrentPopulation.append({"chromosome":self.GenerateRandomChromosome(), "fitness":0.0})
        #self.FillRemaining()
        #self.EvaluatePopulation()
        #self.GenerateNextPopulation()


    def __init__(self, altFitness=Fitness, altPickRandomGene=PickRandomGene, altGenerateRandomChromosome=GenerateRandomChromosome):
        self.Fitness = altFitness
        self.PickRandomGene = altPickRandomGene
        self.GenerateRandomChromosome = altGenerateRandomChromosome
