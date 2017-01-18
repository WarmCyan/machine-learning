# thanks to https://github.com/aymericdamien/TensorFlow-Examples/blob/master/notebooks/3_NeuralNetworks/multilayer_perceptron.ipynb 

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf

# parameters
learning_rate = 0.001
training_epochs = 15
batch_size = 100
display_step = 1

# network stuff
n_hidden_1 = 256
n_hidden_2 = 256
n_input = 784 # (because each image is 28 by 28)
n_classes = 10 # (one for each digit)

x = tf.placeholder("float", [None, n_input]) # input
y = tf.placeholder("float", [None, n_classes]) # output

# uses RELU activation?
# NOTE: remember, x is the input vector
# this is the model creator
def multilayer_perceptron(x, weights, biases):
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)

    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)

    # output layer has linear activation instead? (does this mean no actual
    # "activation" funciton?
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

# weights and bias vectors
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])), # connects input to first hidden layer
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# make the model now
pred = multilayer_perceptron(x, weights, biases)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

init = tf.global_variables_initializer()

# do it!
with tf.Session() as sess:
    sess.run(init)

    # training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        total_batch = int(mnist.train.num_examples/batch_size)
        for i in range(total_batch):
            batch_x, batch_y = mnist.train.next_batch(batch_size)

            # run backprop (optimization op) and cost op
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})

            avg_cost += c / total_batch
            
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(avg_cost))
    print("training finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy: ", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))
                
