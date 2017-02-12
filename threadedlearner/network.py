#print("(importing network...)")
import tensorflow as tf

class Network:


    def __init__(self):
        #print("initializing network...")
        self.sess = tf.InteractiveSession()

        self.x = tf.placeholder(tf.float32, shape=[None,3])
        self.y_ = tf.placeholder(tf.float32, shape=[None, 1])

        self.W = tf.Variable(tf.zeros([3, 1]))
        self.b = tf.Variable(tf.zeros([1]))

        self.y = tf.matmul(self.x, self.W) + self.b

        # cost is just difference in this case
        self.cost = tf.abs(tf.subtract(self.y_, self.y))

        self.train_step = tf.train.GradientDescentOptimizer(.5).minimize(self.cost)

        self.sess.run(tf.global_variables_initializer())
        #print("Network initialized!")


    def feedForward(self, x):
        return self.y.eval(feed_dict={self.x: x})

    def train(self, x, y_):
        self.train_step.run(feed_dict={self.x: x, self.y_: y_})

    def saveNetwork(self, filename):
        saver = tf.train.Saver()
        saver.save(self.sess, "cache/" + filename)
        saver.export_meta_graph("cache/" + filename + ".meta")

    def loadNetwork(self, filename):
        tf.reset_default_graph()
        saver = tf.train.import_meta_graph("cache/" + filename + ".meta")
        saver.restore(self.sess, "cache/" + filename)
        
#print("(network imported)")
