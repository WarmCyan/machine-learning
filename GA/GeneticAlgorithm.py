class GeneticAlgorithm:

    SelectionType = "StochasticUniversal" # "StochasticUniversal", "FitnessProportionate", "Tournament", "RewardBased", "Truncation", "Elitism"
    CrossoverType = "Single" # "Single","Double", "CutSplice", "Uniform"
    CrossoverProbability = 0.2
    MutationProbability = 0.001

    PopulationSize = 1000

    EncodingChart = {} # handled in a wrapper, not here?
    DecodingChart = {} # handled in a wrapper, not here?

    CurrentPopulation = [ ["0100101",0.0] ] # chromosome and fitness
    SortedPopulation = [] # use this as a buffer while evaluating population fitness, then set Current to this
    NextPopulation = []

    # Set by the wrapper. Should accept a chromsome, and should return a float fitness
    def Fitness(self, chromosome):
        print("Checking fitness...")
        return 0.0

    # runs the Fitness on every chromsome in CurrentPopulation and sets its fitness
    def EvaluatePopulation(self):
        for chromsomeEntry in self.CurrentPopulation:
            chromsomeEntry[1] = self.Fitness(chromsomeEntry[0])
            self.AddChromosomeEntryToSorted(chromsomeEntry)

        # all of population evaluated and sorted in SortedPopulation, TODO: do
        # we set current to sorted or just leave it?

    # call this as running evaluate population, and insert wherever this
    # new chromsome has a greater fitness then one at that location
    def AddChromosomeEntryToSorted(self, newChromosomeEntry):
        for i in range(0, len(self.SortedPopulation)):
            chromsomeEntry = self.SortedPopulation[i];
            if newChromosomeEntry[1] >= chromsomeEntry[1]:
                self.SortedPopulation.insert(i, newChromosomeEntry)
                return
            
        # if reached this point, list either empty, or lowest fitness score, so
        # store at end
        self.SortedPopulation.append(newChromosomeEntry)
    
    def GenerateInitialPopulation(self):
        pass

    def GenerateNextPopulation(self):
        self.Selection()
        self.Crossover()       
        self.Mutate()

    def Selection(self):
        pass

    def Crossover(self):
        pass

    def Mutate(self):
        pass

    def __init__(self, altFitness=Fitness):
        self.Fitness = altFitness
        print("running whatever fitness check we have...")
        self.Fitness("10001")

