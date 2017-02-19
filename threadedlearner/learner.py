import sys, os
import tensorflow as tf
import random
import curses
import traceback

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

    for i in range(size):
        choice = random.randint(0, len(queries) - 1)
        query_batch.append(queries[choice])
        answers_batch.append(answers[choice])
    
    return query_batch, answers_batch

#def trainBackground(self, trainingSet, net):
    #net.train(trainingSet[0], trainingSet[1])
    #return net

def display(queue, msg, screen = 0, insertNewLine=True):
    if insertNewLine: queue.put({"content":msg + "\n","loc":screen})
    else: queue.put({"content":msg,"loc":screen})

def disp(q_disp, q_output):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.nodelay(True)
    
    curses.start_color()
    curses.use_default_colors() 

    curses.curs_set(False)

    util = utilities.Utilities(stdscr)

    cur_input = ""

    running = True
    while running:

        # wait for input
        key = util.waitKey()
        if util.exitTriggered:
            q_output.put({"message":"QUIT"})
            running = False
        
        if key != None:
            if key == "!ENTER":
                q_output.put({"message": "input", "data":cur_input})
                cur_input = ""
            else:
                cur_input += str(key)
            
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
        elif msg["message"] == "input":
            q_fg_input.put(msg)
        elif msg["message"] == "request batch":
            q_bg_input.put({"message": "batch response", "data": getBatch(queries, answers, 50000)})
        elif msg["message"] == "request background network":
            q_bg_input.put(msg)
        elif msg["message"] == "background network ready":
            q_fg_input.put(msg)
        elif msg["message"] == "QUIT":
            q_bg_input.put(msg)
            q_fg_input.put(msg)
            display(q_disp, "!!!EXIT!!!")
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
            display(q_disp, "Training batch " + str(backgroundNN.trainingRuns) + "...", 1)
            #display(q_disp, "Set:\n" + str(obj["data"][0]), 1)

            divide_index = int(len(obj["data"][0])*.8)

            training_x = obj["data"][0][0:divide_index]
            training_y = obj["data"][1][0:divide_index]
            testing_x = obj["data"][0][divide_index:]
            testing_y = obj["data"][1][divide_index:]
            
            backgroundNN.train(training_x, training_y)
            backgroundNN.test(training_x, training_y)
            
            display(q_disp, "Trained a batch! Accuracy: " + str(backgroundNN.testAccuracy), 1)
        elif obj["message"] == "request background network":
            display(q_disp, "Saving background network...")
            backgroundNN.saveNetwork("background")
            display(q_disp, "Saved successfully!")
            q_output.put({"message":"background network ready"})
        elif obj["message"] == "QUIT":
            display(q_disp, "Exiting...", 1)
            running = False
        
        #print("Background got " + str(obj))
        #queue.put(obj + 1)

def foreground(q_input, q_output, q_disp):
    try:
        foregroundNN = nn.Network()
        running = True

        display(q_disp, "> ", 0, False)
        while running: 
            obj = None
            
            try:
                obj = q_input.get(True, 1)
            except: pass
            
            if obj == None:
                pass

            elif obj["message"] == "background network ready":
                display(q_disp, "Loading background network...")
                foregroundNN.loadNetwork("background")
                display(q_disp, "Loaded background network\n> ", 0, False)
            
            elif obj["message"] == "input":
                display(q_disp, "Received input: " + obj["data"])

                cmd = obj["data"]
                cmd = cmd.split(" ")

                if cmd[0] == "load":
                    q_output.put({"message":"request background network"})
                    display(q_disp, "Requesting background network...")
                elif len(cmd) == 4:
                    query = [int(cmd[0]), int(cmd[1]), int(cmd[2])]
                    answer = [int(cmd[3])]
                    q_output.put({"message": "store query", "query": query, "answer": answer})

                    result = foregroundNN.feedForward([query])
                    display(q_disp, "Network: " + str(result) + "\n> ", 0, False)
                else:
                    display(q_disp, "Unrecognized command!\n> ", 0, False)
                
            #q_output.put({"Message": "store query", "query": [int(cmdInput[0]), int(cmdInput[1]), int(cmdInput[2])], "answer": [int(cmdInput[3])]})
                
            elif obj["message"] == "QUIT":
                display(q_disp, "Exiting...")
                running = False
                
    except Exception as e: 
        display(q_disp, "FAILED")
        display(q_disp, "Error: " + str(e))
        q_output.put({"message":"QUIT"})
        traceback.print_exc()
        
        #cmdInput = str(cmdInput.split(" "))
        
        #q_output.put({"Message": "store query", "query": [int(cmdInput[0]), int(cmdInput[1]), int(cmdInput[2])], "answer": [int(cmdInput[3])]})



#test = network.Network()


#test.saveNetwork("prev")
#print(test.feedForward([[2,3,4]]))
#test.train([[2,3,4]],[[1]])
#print(test.feedForward([[2,3,4]]))
#test.loadNetwork("prev")
#print(test.feedForward([[2,3,4]]))
