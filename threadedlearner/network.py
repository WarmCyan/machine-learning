#print("(importing network...)")
import tensorflow as tf

class Network:


    def __init__(self):
        #print("initializing network...")
        #self.sess = tf.InteractiveSession()

        #self.x = tf.placeholder(tf.float32, shape=[None,3])
        #self.y_ = tf.placeholder(tf.float32, shape=[None, 1])

        #self.W = tf.Variable(tf.zeros([3, 1]))
        #self.b = tf.Variable(tf.zeros([1]))

        #self.y = tf.matmul(self.x, self.W) + self.b

        # cost is just difference in this case
        #self.cost = tf.abs(tf.subtract(self.y_, self.y))

        #self.train_step = tf.train.GradientDescentOptimizer(.5).minimize(self.cost)

        
        self.sess = tf.InteractiveSession()
        self.assignStructure()
        self.sess.run(tf.global_variables_initializer())
        #print("Network initialized!")

    def assignStructure(self):

        self.x = tf.placeholder(tf.float32, shape=[None,3])
        self.y_ = tf.placeholder(tf.float32, shape=[None, 1])

        self.W = tf.Variable(tf.zeros([3, 1]))
        self.b = tf.Variable(tf.zeros([1]))

        self.y = tf.matmul(self.x, self.W) + self.b

        # cost is just difference in this case
        self.cost = tf.abs(tf.subtract(self.y_, self.y))

        self.train_step = tf.train.GradientDescentOptimizer(.5).minimize(self.cost)


    def feedForward(self, x):
        return self.y.eval(feed_dict={self.x: x})

    def train(self, x, y_):
        self.train_step.run(feed_dict={self.x: x, self.y_: y_})

    def saveNetwork(self, filename):
        saver = tf.train.Saver()
        saver.save(self.sess, "cache/" + filename)
        #saver.export_meta_graph("cache/" + filename + ".meta")

    def loadNetwork(self, filename):
        self.sess = tf.InteractiveSession()
        self.assignStructure()
        #tf.reset_default_graph()
        saver = tf.train.import_meta_graph("cache/" + filename + ".meta")
        #self.sess = tf.InteractiveSession()
        saver.restore(self.sess, "cache/" + filename)
        #saver.restore(self.sess, tf.train.latest_checkpoint('./'))
        
#print("(network imported)")
