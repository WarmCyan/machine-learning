#print("(importing network...)")
import tensorflow as tf

class Network:


    def __init__(self):
        pass
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

        self.trainingRuns = 0
        self.testAccuracy = 0.0
        #print("Network initialized!")

    def assignStructure(self):

        self.x = tf.placeholder(tf.float32, shape=[None,3])
        self.y_ = tf.placeholder(tf.float32, shape=[None, 1])

        self.W = tf.Variable(tf.zeros([3, 1]))
        self.b = tf.Variable(tf.zeros([1]))

        self.y = tf.matmul(self.x, self.W) + self.b

        # cost is just difference in this case
        self.cost = tf.abs(tf.subtract(self.y_, self.y))

        #self.train_step = tf.train.GradientDescentOptimizer(.001).minimize(self.cost)
        self.train_step = tf.train.GradientDescentOptimizer(.001).minimize(self.cost)

        self.test_step = tf.reduce_mean(tf.cast(tf.equal(tf.round(self.y), self.y_), tf.float32))


    def feedForward(self, x):
        return self.y.eval(feed_dict={self.x: x})

    def train(self, x, y_):
        self.trainingRuns += 1
        self.train_step.run(feed_dict={self.x: x, self.y_: y_})

    def test(self, x, y_):
        self.testAccuracy = self.test_step.eval(feed_dict={self.x: x, self.y_: y_})

    def saveNetwork(self, filename):
        #tf.add_to_collection('vars', self.x)
        #tf.add_to_collection('vars', self.y_)
        #tf.add_to_collection('vars', self.W)
        #tf.add_to_collection('vars', self.b)
        #tf.add_to_collection('vars', self.y)
        saver = tf.train.Saver()
        saver.save(self.sess, "cache/" + filename)
        #saver.export_meta_graph("cache/" + filename + ".meta")

    def loadNetwork(self, filename):
        #tf.reset_default_graph()
        #self.sess = tf.InteractiveSession()
        #self.sess.close()
        #self.sess = tf.InteractiveSession()
        #self.assignStructure()
        #self.sess.run(tf.global_variables_initializer())
        #saver = tf.train.import_meta_graph("cache/" + filename + ".meta")
        #self.sess = tf.InteractiveSession()
        #saver.restore(self.sess, "cache/" + filename)
        #saver.restore(self.sess, tf.train.latest_checkpoint('./'))
        
        #self.sess.close()
        #self.sess = tf.InteractiveSession()
        #saver = tf.train.import_meta_graph("cache/" + filename + ".meta")
        #tf.train.import_meta_graph("cache/" + filename + ".meta")
        saver = tf.train.Saver()
        saver.restore(self.sess, "cache/" + filename)
        
#print("(network imported)")
