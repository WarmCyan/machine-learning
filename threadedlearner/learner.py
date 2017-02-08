import tensorflow as tf

import multiprocessing as mp


import network
#import Queue

class Learner:

    def __init__(self):
        pass

prev_queries = []
prev_answers = []


# randomly select some elements from prev_queries
def getBatch():
    pass

def background():
    backNet = network.Network()

    
    pass


#test = network.Network()


#test.saveNetwork("prev")
#print(test.feedForward([[2,3,4]]))
#test.train([[2,3,4]],[[1]])
#print(test.feedForward([[2,3,4]]))
#test.loadNetwork("prev")
#print(test.feedForward([[2,3,4]]))
