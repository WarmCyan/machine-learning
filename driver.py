import NNet as net

nn = net.NeuralNetwork(2,1,3,1)
nn.initTheanoFunctions()
#nn.readTrainingData("datasmaller.txt")
#nn.readTrainingData("data.txt")
nn.readTrainingData("bigdata.txt")

nn.generateWeights()
#nn.runFeedForward([[1.0,0.0]])
#nn.backPropogate([[1.0]]);

#nn.calculateRunError()

nn.train()

print "Initial weights:"
nn.printInitialWeights()
print "Final weights:"
nn.printWeights()
