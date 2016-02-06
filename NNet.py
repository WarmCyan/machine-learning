print "(Running imports...)"
import theano 
import theano.tensor as t
import numpy
print "(Imports complete!)"

# NOTE: For now, weights will be randomly initialized

class NeuralNetwork():
	
	# member variables
	trainingInputs = []
	trainingOutputs = []
	weights = []

	inputs = 0
	layers = 0
	layerNeuronCount = 0
	outputs = 0

	# necessary training variables
	netOutput = 0;
	
	
	# construction
	def __init__(self, inpNum, hiddenLayerNum, hiddenLayerNeurons, outNum):
		print "Network shape initialized: " + str(inpNum) + " inputs, " + str(hiddenLayerNum) + " hidden layers, " + str(hiddenLayerNeurons) + " neurons per hidden layer, " + str(outNum) + " outputs"
		self.inputs = inpNum
		self.layers = hiddenLayerNum
		self.layerNeuronCount = hiddenLayerNeurons
		self.outputs = outNum
		
	# setup and compile the necessary theano functions
	def initTheanoFunctions(self):
		print "(Compiling theano functions...)"

		mat_incoming = t.dmatrix('mat_incoming') # layer inputs
		mat_weights = t.dmatrix('mat_weights') # layer connection weights
		mat_presig = t.dot(mat_incoming, mat_weights) # dot product of inputs with weights (no sigmoid yet)

		mat_outputs = 1 / (1 + t.exp(-mat_presig)) # apply sigmoid

		self.feedForward = theano.function([mat_incoming, mat_weights], mat_outputs)

		print "(Functions ready!)"

	# expects csv file
	def readTrainingData(self, fileName):
		lines = [line.strip() for line in open(fileName)]
		for line in lines:
			csv = line.split(",")

			# get training inputs
			inputArray = numpy.asarray([[]])
			for i in range(0,self.inputs):
				value = float(csv[i])
				inputArray = numpy.concatenate((inputArray, [[value]]), 1) # 1 specifies axis (adds col, not row)
			self.trainingInputs.append(inputArray)

			# get training outputs
			outputArray = numpy.asarray([[]])
			for i in range(0 + self.inputs, self.inputs + self.outputs):
				value = float(csv[i])
				outputArray = numpy.concatenate((outputArray, [[value]]), 1)
			self.trainingOutputs.append(outputArray)	
			
		# print self.trainingInputs
		# print self.trainingOutputs

	# TODO: one input to hidden matrix, (amount) hidden to hidden, hidden to out matrix
	def generateWeights(self):
		
		# input to first hidden layer (inputs x hiddenLayerNodes)
		weights_in_hidden = numpy.random.rand(self.inputs, self.layerNeuronCount)
		weights_in_hidden = weights_in_hidden#*2 - 1 # normalize weights (-1,1)
		self.weights.append(weights_in_hidden)
		
		for i in range(0,self.layers - 1): # input
			weights_hidden_hidden = numpy.random.rand(self.layerNeuronCount, self.layerNeuronCount)
			weights_hidden_hidden = weights_hidden_hidden#*2 - 1 # normalize weights (-1,1)
			self.weights.append(weights_hidden_hidden)

		# final hidden to output layer (hiddenLayerNodes x outputs)
		weights_hidden_out = numpy.random.rand(self.layerNeuronCount, self.outputs)
		weights_hidden_out = weights_hidden_out#*2 - 1 # normalize weights (-1,1)
		self.weights.append(weights_hidden_out)

		for i in range(0, len(self.weights)):
			print self.weights[i]

	# runs single input through
	def runFeedForward(self, inputArray):
		# run first feedforward

		#for i in range(0, len(self.trainingInputs)):
			#print self.trainingInputs[i]

		#currentIn = self.trainingInputs[0] # USED THIS ONE
		currentIn = inputArray

		# input and hidden layers
		print "---------"
		for i in range(0, len(self.weights)-1):
			currentWeights = self.weights[i]
			currentIn = self.feedForward(currentIn, currentWeights)
			print currentIn

		# final layer
		output = self.feedForward(currentIn, self.weights[len(self.weights) - 1])
		
		print "---------"
		print output
		
