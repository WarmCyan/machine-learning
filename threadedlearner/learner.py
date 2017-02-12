import sys, os
import tensorflow as tf
import random
import curses

import multiprocessing as mp


import network as nn
import utilities
#import Queue

number1 = 1
number2 = 2
number3 = 3

prev_queries = []
prev_answers = []

batchSize = 5

#backgroundNN = None
#foregroundNN = None

def initialize():
    
    q_bg_input = mp.Queue();
    q_fg_input = mp.Queue();
    q_output = mp.Queue();
    q_disp = mp.Queue();
    
    disp_proc = mp.Process(target=disp, args=(q_disp,q_output,))
    io_proc = mp.Process(target=io, args=(q_fg_input, q_bg_input,q_output,q_disp,))
    bg_proc = mp.Process(target=background, args=(q_bg_input,q_output,q_disp,))
    fg_proc = mp.Process(target=foreground, args=(q_fg_input,q_output,q_disp,))

    disp_proc.start()
    io_proc.start()
    bg_proc.start()
    fg_proc.start()


    #util.print("yup, yup, yup, main process here")
    running = True
    #while running:
        #cmdInput = input("> ")
       
        #cmdInput = str(cmdInput.split(" "))
        
        #q_output.put({"Message": "store query", "query": [int(cmdInput[0]), int(cmdInput[1]), int(cmdInput[2])], "answer": [int(cmdInput[3])]})
    

    bg_proc.join()
    fg_proc.join()
    io_proc.join()
    disp_proc.join()

    print("Goodbye!")

    
def getBatch(queries, answers, size):
    query_batch = []
    answers_batch = []

    for i in range(batchSize):
        choice = random.randint(0, len(queries) - 1)
        query_batch.append(queries[choice])
        answers_batch.append(answers[choice])
    
    return query_batch, answers_batch

#def trainBackground(self, trainingSet, net):
    #net.train(trainingSet[0], trainingSet[1])
    #return net

def disp(q_disp, q_output):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.nodelay(True)
    
    curses.start_color()
    curses.use_default_colors() 

    util = utilities.Utilities(stdscr)

    running = True
    while running:

        # wait for input
        util.wait()
        if util.exitTriggered:
            q_output.put({"message":"QUIT"})
            running = False
            
        # check display queue
        msg = None
        try: msg = q_disp.get_nowait()
        except: pass
        
        if msg != None:
            if msg["content"] == "!!!EXIT!!!":
                running = False
            else:
                util.print(msg["content"], msg["loc"])

    
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def io(q_fg_input, q_bg_input, q_output, q_disp):

    queries = [[1,2,3]]
    answers = [[0]]

    running = True
    while running:
        msg = q_output.get()
        if msg["message"] == "store query":
            queries.append(msg["query"])
            answers.append(msg["answer"])
        elif msg["message"] == "request batch":
            q_bg_input.put({"message": "batch response", "data": getBatch(queries, answers, 5)})
        elif msg["message"] == "QUIT":
            q_bg_input.put(msg)
            q_disp.put({"content":"Exiting...", "loc":0})
            running = False


def background(q_input, q_output, q_disp):
    backgroundNN = nn.Network()
    running = True
    while running: 
        obj = None
        try:
            obj = q_input.get(True, 1)
        except: pass
        if obj == None:
            q_output.put({"message":"request batch"})
        elif obj["message"] == "batch response":
            #util.print("Training...",1)
            #q_output.put({"message":"print", "data":"Training...", "loc": 1})
            q_disp.put({"content":"Training...\n", "loc":1})
            backgroundNN.train(obj["data"][0], obj["data"][1])
            #q_output.put({"message":"print", "data":"Trained a batch!", "loc": 1})
            #util.print("Trained a batch!", 1)
            q_disp.put({"content":"Trained a batch!\n", "loc":1})
        elif obj["message"] == "QUIT":
            q_disp.put({"content":"Exiting...", "loc":0})
            running = False
        
        #print("Background got " + str(obj))
        #queue.put(obj + 1)

def foreground(q_input, q_output, q_disp):
    foregroundNN = nn.Network()
    running = True
    #q_output.put({"message":"print", "data":"Fg rules!", "loc": 0})
    q_disp.put({"content":"FG rules!!!", "loc": 0})
    #while running: 
        #cmdInput = input("> ")
        #print("> ")
        #cmdinput = stdin.readline()
        
        #cmdInput = str(cmdInput.split(" "))
        
        #q_output.put({"Message": "store query", "query": [int(cmdInput[0]), int(cmdInput[1]), int(cmdInput[2])], "answer": [int(cmdInput[3])]})



#test = network.Network()


#test.saveNetwork("prev")
#print(test.feedForward([[2,3,4]]))
#test.train([[2,3,4]],[[1]])
#print(test.feedForward([[2,3,4]]))
#test.loadNetwork("prev")
#print(test.feedForward([[2,3,4]]))
