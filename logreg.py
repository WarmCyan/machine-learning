import numpy
import theano
import theano.tensor as t

rng = numpy.random

N = 400 # sample number
feats = 784 # dimensionality of features????
D = (rng.randn(N, feats), rng.randint(size=N, low=0, high=2))

training_steps = 10000

x = t.matrix('x')
y = t.vector('y')
w = theano.shared(rng.randn(784), name='w')
b = theano.shared(0., name='b')

print "initial model:"
print w.get_value(), b.get_value()


# theano expression graph???
p_1 = 1 / (1 + t.exp(-t.dot(x,w)-b)) # Prob that target is 1
prediction = p_1 > 0.5 # prediction threshold
xent = -y*t.log(p_1) - (1-y)*t.log(1-p_1) # cross-entropy loss func
cost = xent.mean() + .01 * (w**2).sum() # cost to minimize
gw, gb = t.grad(cost, [w,b])


#compile the funciton
train = theano.function(inputs=[x,y], outputs=[prediction,xent], updates={w : w-0.1*gw, b : b-0.1*gb})
predict = theano.function(inputs=[x], outputs=prediction)


#train
for i in range(training_steps):
	pred, err = train(D[0], D[1])

print "Final model:"
print w.get_value(), b.get_value()
print "target values for D: ", D[1]
print "predictions on D: ", predict(D[0])

