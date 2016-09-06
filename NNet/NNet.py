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

	initialWeights = []

	lastWeights = []

	inputs = 0
	layers = 0
	layerNeuronCount = 0
	outputs = 0

	learningRate = 2; # (alpha)

	# necessary training variables
	
	
	
	# saved data from feed forward for backpropogation
	#lastLayers = numpy.asarray([[]])
	run_inputs = []; # this should NOT be run through a logistic, correct?
	run_layerNodeValues = []; # no sigmoid
	run_layerNodeResults = []; # AFTER sigmoid (store this so don't have to keep calculating it)
	run_outputs = 0;
	run_outputTargets = 0;	
	run_error = 0;
	
	
	# construction
	def __init__(self, inpNum, hiddenLayerNum, hiddenLayerNeurons, outNum):
		#print "Network shape initialized: " + str(inpNum) + " inputs, " + str(hiddenLayerNum) + " hidden layers, " + str(hiddenLayerNeurons) + " neurons per hidden layer, " + str(outNum) + " outputs"
		self.inputs = inpNum
		self.layers = hiddenLayerNum
		self.layerNeuronCount = hiddenLayerNeurons
		self.outputs = outNum
		
	# setup and compile the necessary theano functions
	def initTheanoFunctions(self):
		print "(Compiling theano functions...)"

		# basic node value finding function (prev layer dot weights)
		# TODO: add bias matrix parameter to be passed in as well?
		mat_incoming = t.dmatrix('mat_incoming') # layer inputs
		mat_weights = t.dmatrix('mat_weights') # layer connection weights
		mat_nodeValues = t.dot(mat_incoming, mat_weights) # dot product of inputs with weights (no sigmoid yet) This is first half value of each node
		
		self.feedNodes = theano.function([mat_incoming, mat_weights], mat_nodeValues)
		
		# sigmoid logistic function
		mat_incoming = t.dmatrix('mat_incoming')
		mat_logisticSigmoid = 1 / (1 + t.exp(-mat_incoming))
		
		self.logisticSigmoid = theano.function([mat_incoming], mat_logisticSigmoid)
		
		# derivative functions!
		
		# d(error) / d(logistic[layerOutput])
		mat_outputResults = t.dmatrix('mat_outputResults')
		mat_target = t.dmatrix('mat_target')
		mat_dErrorDOutputResults = -(mat_target - mat_outputResults)

		self.dErrorDOutputResults = theano.function([mat_outputResults, mat_target], mat_dErrorDOutputResults)

		# sigmoid logistic derivative
		mat_sigmoid = t.dmatrix('mat_sigmoid')
		#mat_ones = shared(numpy.ones(t.shape(mat_signmoid)))
		mat_dSigmoidDValues = numpy.asarray(mat_sigmoid) * numpy.asarray(1 - numpy.asarray(mat_sigmoid))
		#mat_dSigmoidDValues = mat_sigmoid * (numpy.ones(t.shape(mat_sigmoid)) - mat_sigmoid)
		#mat_dSigmoidDValues = mat_sigmoid * (1 - 

		self.dSigmoidDValues = theano.function([mat_sigmoid], mat_dSigmoidDValues)

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
			
		#print self.trainingInputs
		#print self.trainingOutputs

	# TODO: one input to hidden matrix, (amount) hidden to hidden, hidden to out matrix
	def generateWeights(self):
		
		# input to first hidden layer (inputs x hiddenLayerNodes)
		weights_in_hidden = numpy.random.rand(self.inputs, self.layerNeuronCount)
		weights_in_hidden = weights_in_hidden*2 - 1 # normalize weights (-1,1)
		self.weights.append(weights_in_hidden)
		
		for i in range(0,self.layers - 1): # input
			weights_hidden_hidden = numpy.random.rand(self.layerNeuronCount, self.layerNeuronCount)
			weights_hidden_hidden = weights_hidden_hidden*2 - 1 # normalize weights (-1,1)
			self.weights.append(weights_hidden_hidden)

		# final hidden to output layer (hiddenLayerNodes x outputs)
		weights_hidden_out = numpy.random.rand(self.layerNeuronCount, self.outputs)
		weights_hidden_out = weights_hidden_out*2 - 1 # normalize weights (-1,1)
		self.weights.append(weights_hidden_out)

		for i in range(0, len(self.weights)):
			print "Weights:\n" + str(self.weights[i])
		
		self.initialWeights = list(self.weights)

	# assumes that run_outputs and run_outputTargets are already set
	def calculateRunError(self):
		mat_errors = .5 * (numpy.asarray(self.run_outputTargets - self.run_outputs) ** 2)
		self.run_error = numpy.sum(mat_errors)

	# runs single input through
	def runFeedForward(self, inputArray):
		# run first feedforward

		self.run_inputs = numpy.asarray(inputArray)
		self.run_layerNodeValues = [];
		self.run_layerNodeResults = [];

		#for i in range(0, len(self.trainingInputs)):
			#print self.trainingInputs[i]

		#currentIn = self.trainingInputs[0] # USED THIS ONE
		currentIn = inputArray

		# input and hidden layers
		#print "---------"
		for i in range(0, len(self.weights)):
			currentWeights = self.weights[i]
		

			
			currentIn = self.feedNodes(currentIn, currentWeights)
			#currentIn = self.feedForward(currentIn, currentWeights)
			
			if (numpy.isnan(currentIn).any()):
				print "CURRENT IN IS NULL RIGHT AFTER FEED NODES!!!! -------------------------"
				print "weights:"
				print self.weights
				print "layernodevalues:"
				print self.run_layerNodeValues
				print "LAST weights:"
				print self.lastWeights

			self.run_layerNodeValues.append(currentIn)
			
			currentIn = self.logisticSigmoid(currentIn);

			self.run_layerNodeResults.append(currentIn)

			if (numpy.isnan(currentIn).any()):
				print "CURRENT IN IS NULL"
				print "weights:"
				print self.weights
				print "layernodevalues:"
				print self.run_layerNodeValues

			#if (i == len(self.weights) - 1):
				#self.run_outputs = currentIn
			
			#print "Layer results:\n" + str(currentIn)

		# explicitly assign outputs for ease
		self.run_outputs = self.run_layerNodeResults[-1]

		# final layer
		#output = self.feedForward(currentIn, self.weights[len(self.weights) - 1])
		
		#self.lastOutput = output
		
		#print "---------"
		#print "Net outputs:\n" + str(self.run_outputs)

	# remember, strucuture is 2 3 1	
		
	# target array should be same dimension as lastOutput, obviously
	def backPropogate(self, targetArray):
		
		self.lastWeights = list(self.weights)
		self.run_outputTargets = targetArray;
		
		#print "Layer node values:\n" + str(self.run_layerNodeValues)
		#print "Layer node results:\n" + str(self.run_layerNodeResults)
		
		#print "\n\n---- Output layer weight adjustment ----"

		stepOne = self.dErrorDOutputResults(self.run_outputs, self.run_outputTargets)

		#print "Step 1:"
		#print stepOne

		stepTwo = self.dSigmoidDValues(self.run_outputs)

		#print "\nStep 2:"
		#print stepTwo

		stepThree = self.run_layerNodeResults[-2]

		#print "\nStep 3:"
		#print stepThree

		finalStep = stepThree.transpose() * (numpy.asarray(stepOne) * numpy.asarray(stepTwo))

		#print "\nFinal affect of weights on error:"
		#print finalStep

		#finalStep = stepOne * stepTwo * self.run_layerNodeResults[-2]
		#print "\n[2] -- Final affect of weights on error:"
		#print finalStep

		# apply final step to weights
		#print "\n\n"
		#print "Old weights:"
		#print self.weights[-1]
		#print self.weights

		self.weights[-1] = self.weights[-1] - self.learningRate * finalStep
		if (numpy.isnan(self.weights[-1]).any()):
			print "WEIGHTS -1 WAS NAN"
			print "finalstep:"
			print finalStep
			print "Step 3:"
			print stepThree
			print "Step 2:"
			print stepTwo
			print "Step 1:"
			print stepOne
		
		#print "\nNew weights:"
		#print self.weights[-1]
		

		#print "\n\n---- Input layer weight adjustment ----"
		stepThree2 = self.weights[-1]
	
		#print "(Steps 1-2 same as above)"
		#print "Step 3:"
		#print stepThree
		
		stepFour = self.dSigmoidDValues(self.run_layerNodeResults[-2])

		#print "\nStep 4"
		#print stepFour

		stepFive = self.run_inputs

		#print "\nStep 5"
		#print stepFive

		finalStep2 = stepFive.transpose() * numpy.asmatrix(numpy.asarray(stepFour) * numpy.asarray((numpy.asarray(stepOne) * numpy.asarray(stepTwo)) * stepThree2.transpose()))

		#print self.run_layerNodeValues[-2]
		#print stepFour

		#print "\nFinal affect of weights on error:"
		#print finalStep

		# apply final step to weights
		#print "\n\n"
		#print "Old weights:"
		#print self.weights[-2]

		self.weights[-2] = self.weights[-2] - self.learningRate * finalStep2
		if (numpy.isnan(self.weights[-2]).any()):
			print "WEIGHTS -2 WAS NAN"
			print "finalstep2:"
			print finalStep2
			print "Step 5:"
			print stepFive
			print "Step 4:"
			print stepFour

			print "\t\t\tPOTENTIAL PROBLEM?"
			print "layerNodeValues before put into step four"
			print self.run_layerNodeValues[-2]
			
			print "Step 3 (2):"
			print stepThree2
			print "Step 2:"
			print stepTwo
			print "Step 1:"
			print stepOne
		
		#print "\nNew weights:"
		#print self.weights[-2]

	
	def train(self):
		for i in range(0, len(self.trainingInputs)):
			#print "Expected: " + str(self.trainingOutputs[i])
			self.runFeedForward(self.trainingInputs[i])
			self.backPropogate(self.trainingOutputs[i])
			#print "Network: " + str(self.run_outputs)
			self.calculateRunError()
			#print "Set error: " + str(self.run_error)
			if (i % 100 == 0):
				print "Training set " + str(i) + ": " + "exp: " + str(self.trainingOutputs[i]) + " net: " + str(self.run_outputs) + " err: " + str(self.run_error)
			if numpy.isnan(self.run_outputs):
				print "ERROR DETECTED"
				print self.weights
				print self.run_inputs
				print self.run_layerNodeValues
				print self.run_layerNodeResults
				print self.run_outputs
				break;

		print "\nFinished training!\n"
		

	# debugging/info functions
	# (later print net node info HERE, instead of in the functions)
	def printWeights(self):
		for i in range(0, len(self.weights)):
			print self.weights[i]
			
	def printInitialWeights(self):
		for i in range(0, len(self.initialWeights)):
			print self.initialWeights[i]

