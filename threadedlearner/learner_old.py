import tensorflow as tf
import random

import multiprocessing as mp


import network as nn
#import Queue

class Learner:

    number1 = 1
    number2 = 2
    number3 = 3

    prev_queries = []
    prev_answers = []

    batchSize = 5

    backgroundNN = None
    foregroundNN = None

    def __init__(self, primary=False):
        #self.foregroundNN = nn.Network()
        #self.backgroundNN = nn.Network()

        queue1 = mp.Queue();
        queue2 = mp.Queue()
        
        back = mp.Process(target=self.background)
        fore = mp.Process(target=self.foreground)

        back.start()
        fore.start()

        back.join()
        fore.join()
        print("Actual: " + str(self.number1))
        
    def getBatch(self):
        query_batch = []
        answers_batch = []

        for i in range(self.batchSize):
            choice = random(0, len(self.prev_queries) - 1)
            query_batch.append(self.prev_queries[choice])
            answers_batch.append(self.prev_answers[choice])
        
        return query_batch, answers_batch

    #def trainBackground(self, trainingSet, net):
        #net.train(trainingSet[0], trainingSet[1])
        #return net
    
    def background(self, queue):
        self.number1 = 0 
        print("back: " + str(self.number1))

    def foreground(self, queue):
        self.number1 = -1
        print("fore: " + str(self.number1))
    

#test = network.Network()


#test.saveNetwork("prev")
#print(test.feedForward([[2,3,4]]))
#test.train([[2,3,4]],[[1]])
#print(test.feedForward([[2,3,4]]))
#test.loadNetwork("prev")
#print(test.feedForward([[2,3,4]]))
