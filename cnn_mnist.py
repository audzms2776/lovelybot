import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import random
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

learning_rate = 0.001
training_epochs = 15
batch_size = 100

X = tf.placeholder(tf.float32, [None, 784], name='x-input')
X_img = tf.reshape(X, [-1, 28, 28, 1])
Y = tf.placeholder(tf.float32, [None, 10], name='y-input')

# 1 layer
with tf.name_scope('layer1') as scope1:
    W1 = tf.Variable(tf.random_normal([3, 3, 1, 15], stddev=0.01))
    L1 = tf.nn.conv2d(X_img, W1, strides=[1, 1, 1, 1], padding='SAME')
    tf.summary.histogram('conv1', L1)
    L1 = tf.nn.relu(L1)
    tf.summary.histogram('relu1', W1)
    L1 = tf.nn.max_pool(L1, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')
    tf.summary.histogram('pool1', W1)

    tf.summary.histogram('weight1', W1)

# 2 layer
with tf.name_scope('layer1') as scope2:
    W2 = tf.Variable(tf.random_normal([3, 3, 15, 30], stddev=0.01))
    L2 = tf.nn.conv2d(L1, W2, strides=[1, 1, 1, 1], padding='SAME')
    tf.summary.histogram('conv2', L1)
    L2 = tf.nn.relu(L2)
    tf.summary.histogram('relu2', L1)
    L2 = tf.nn.max_pool(L2, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')
    tf.summary.histogram('pool2', L1)
    L2_flat = tf.reshape(L2, [-1, 7 * 7 * 30])
    tf.summary.histogram('weight1', W1)

# 3 layer
with tf.name_scope('layer3') as scope3:
    W3 = tf.get_variable('W3', shape=[7 * 7 * 30, 10],
                         initializer=tf.contrib.layers.xavier_initializer())
    b = tf.Variable(tf.random_normal([10]))
    hypo = tf.matmul(L2_flat, W3) + b

    tf.summary.histogram('weight3', W3)
    tf.summary.histogram('bias1', b)
    tf.summary.histogram('hypo', hypo)

print('hypo ', hypo.shape)
print('Y ', Y.shape)

with tf.name_scope('cost') as scope5:
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypo,
                                                                  labels=Y))
    tf.summary.scalar('cost', cost)

with tf.name_scope('train') as scope6:
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

time = 0
for epoch in range(training_epochs):
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter("./cnn_log/cnn_mnist")
    writer.add_graph(sess.graph)

    total_batch = int(mnist.train.num_examples / batch_size)

    for i in range(total_batch):
        batch_xs, batch_ys = mnist.train.next_batch(batch_size)
        feed_dict = {X: batch_xs, Y: batch_ys}
        summary, c, _ = sess.run([merged_summary, cost, optimizer], feed_dict=feed_dict)
        writer.add_summary(summary, global_step=time)
        time += 1

