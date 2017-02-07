import tensorflow as tf

import multiprocessing as mp
#import Queue

inputhistory = []
answerhistory = []

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, shape=[None, 3])
y_ = tf.placeholder(tf.float32, shape=[None, 1])


W = tf.Variable(tf.zeros([3, 1]))
b = tf.Variable(tf.zeros([1]))

y = tf.matmul(x, W) + b

# cost is just difference in this case
cost = tf.abs(tf.subtract(y_, y))

train_step = tf.train.GradientDescentOptimizer(.5).minimize(cost)
sess.run(tf.global_variables_initializer())

train_step.run(feed_dict={x: [[2,3,4]], y_: [[1]]})
print(y.eval(feed_dict={x: [[2, 3, 4]]}))
train_step.run(feed_dict={x: [[3,4,5]], y_: [[2]]})
print(y.eval(feed_dict={x: [[2, 3, 4]]}))
train_step.run(feed_dict={x: [[2,2,3]], y_: [[1]]})
print(y.eval(feed_dict={x: [[2, 3, 4]]}))

print("Yup, we're good now")
