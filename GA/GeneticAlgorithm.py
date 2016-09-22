import random

class GeneticAlgorithm:

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


    CurrentPopulation = [ { "chromosome":['s', 'a', 'm', 'p', 'l', 'e'], "fitness":0.0 } ]
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

    # Set by the wrapper. Should accept a chromsome, and should return a float fitness
    def Fitness(self, chromosome):
        print("Checking fitness...")
        return 0.0




    # runs the Fitness on every chromsome in CurrentPopulation and sets its fitness
    def EvaluatePopulation(self):
        for chromsomeEntry in self.CurrentPopulation:
            chromsomeEntry["fitness"] = self.Fitness(chromsomeEntry["chromosome"])
            self.AddChromosomeEntryToSorted(chromsomeEntry)

        # all of population evaluated and sorted in SortedPopulation, TODO: do
        # we set current to sorted or just leave it?

    # call this as running evaluate population, and insert wherever this
    # new chromsome has a greater fitness then one at that location
    def AddChromosomeEntryToSorted(self, newChromosomeEntry):
        for i in range(0, len(self.SortedPopulation)):
            chromsomeEntry = self.SortedPopulation[i];
            if newChromosomeEntry["fitness"] >= chromsomeEntry["fitness"]:
                self.SortedPopulation.insert(i, newChromosomeEntry)
                return
            
        # if reached this point, list either empty, or lowest fitness score, so
        # store at end
        self.SortedPopulation.append(newChromosomeEntry)
    

    def GenerateNextPopulation(self):
        self.Selection()
        self.Crossover()       
        self.Mutate()
        #self.CurrentPopulation = self.NextPopulation

    def FillRemaining(self):
        pass

    def Selection(self):
        if self.SelectionType == "Elitism":
            for i in range(0, self.ElitismSize):
                self.SelectedParents.append(self.SortedPopulation[i]["chromsome"])

    def Crossover(self):
        while len(SelectedParents) > 0:
            parent1 = SelectedParents[len(SelectedParents) - 1]
            parent2 = SelectedParents[len(SelectedParents) - 2]
            
            crossoverRoll = random.random()

            child1 = []
            child2 = []
            
            if crossoverRoll > self.CrossoverProbability:
                child1 = parent1
                child2 = parent2
            else:
                if self.CrossoverType == "Single":
                    # get two lengths, and get a random number that is less than
                    # either (minimum)
                    len1 = len(parent1)
                    len2 = len(parent2)
                    minlen = min(len1, len2)

                    crossPoint = random.uniform(0, minlen)

                    # carry out the crossover
                    child1 = parent1[0:crossPoint]
                    child1 += parent2[crossPoint:len2]
                    child2 = parent2[0:crossPoint]
                    child2 +=parent1[crossPoint:len1]

            # remove parents and add children to new population
            del SelectedParents[len(SelectedParents) - 1]
            del SelectedParents[len(SelectedParents) - 2]
            self.NextPopulation.append({"chromsome":child1, "fitness":0.0})
            self.NextPopulation.append({"chromsome":child2, "fitness":0.0})

    def Mutate(self):
        pass


    #def SetTournamentSelection(self, tournamentSize=500):
    def SetElitismSelection(self, selectionSize=500):
        self.SelectionType = "Elitism"
        self.ElitismSize = selectionSize


    def RunGeneration():
        # generate population that doesn't exist
        while len(CurrentPopulation) < self.PopulationSize:
            CurrentPopulation.append({"chromsome":self.GenerateRandomChromosome(), "fitness":0.0})

    def __init__(self, altFitness=Fitness, altPickRandomGene=PickRandomGene, altGenerateRandomChromosome=GenerateRandomChromosome):
        self.Fitness = altFitness
        self.RandomGene = altPickRandomGene
        self.GenerateRandomChromosome = altGenerateRandomChromosome
