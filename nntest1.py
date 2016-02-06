print "Importing stuffs..."

import theano
import theano.tensor as t
import numpy
import numpy.random as rng # random number generator

#rng.permutation(3) # random generator for hidden layer values

# ----- theano stuff! -----

print "Compiling stuffs..."

# first theano matrices
inputs = t.dmatrix('inputs') # inputs
weights1 = t.dmatrix('weights1') # first layer weights
presig1 = t.dot(inputs, weights1) # outputs before sigmoid
# out1 = t.dot(inputs, weights1) # hidden layer outputs
out1 = 1 / (1 + t.exp(-presig1))

# first layer function
f1 = theano.function([inputs,weights1], out1)

# second layer weights
weights2 = t.dmatrix('weights2')

# end result outputs
presig2 = t.dot(out1, weights2) # outputs before sigmoid
# outputs = t.dot(out1, weights2)
outputs = 1 / (1 + t.exp(-presig2))

# end result calculator function
f2 = theano.function([out1,weights2], outputs)



# ----- execution stuff! -----

def feedForward(mat_input, mat_weights1, mat_weights2):
	mat_hiddenLayer = f1(mat_input, mat_weights1)
	finalLayer = f2(mat_hiddenLayer, mat_weights2)
	return finalLayer

print "Executing stuffs!"

# matricies!
lmat_input = numpy.asarray([[10,-5]])
lmat_weights1 = numpy.asarray([
	[5,3,7],
	[4,5,4]])
lmat_weights2 = numpy.asarray([
	[-2],
	[7],
	[-3]])

#mat_hiddenLayer = f1(mat_input,mat_weights1)
# print mat_hiddenLayer # DEBUG
#finalLayer = f2(mat_hiddenLayer, mat_weights2)
# print "-----final----- " 
#print finalLayer

result = feedForward(lmat_input, lmat_weights1, lmat_weights2)
print result
