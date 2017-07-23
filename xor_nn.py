import tensorflow as tf
import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# with tf.device('/gpu:0') as ss:
# data
x_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
y_data = np.array([[0], [1], [1], [0]], dtype=np.float32)

X = tf.placeholder(tf.float32, [None, 2])
Y = tf.placeholder(tf.float32, [None, 1])

with tf.name_scope('layer1') as scope1:
    # model
    W1 = tf.Variable(tf.random_normal([2, 20]), name='weight1')
    b1 = tf.Variable(tf.random_normal([20]), name='bias1')
    layer1 = tf.sigmoid(tf.matmul(X, W1) + b1)

    W1_hist = tf.summary.histogram('weight1', W1)
    b1_hist = tf.summary.histogram('bias1', b1)
    layer1_hist = tf.summary.histogram('layer1', layer1)

with tf.name_scope('layer2') as scope2:
    # model
    W2 = tf.Variable(tf.random_normal([20, 1]), name='weight2')
    b2 = tf.Variable(tf.random_normal([1]), name='bias2')
    hypo = tf.sigmoid(tf.matmul(layer1, W2) + b2)

    W2_hist = tf.summary.histogram('weight2', W2)
    b2_hist = tf.summary.histogram('bias2', b2)
    layer2_hist = tf.summary.histogram('layer2', hypo)

with tf.name_scope('cost') as scope3:
    # optimization
    cost = -tf.reduce_mean(Y * tf.log(hypo) + (1 - Y) * tf.log(1 - hypo))
    cost_num = tf.summary.scalar('cost', cost)

with tf.name_scope('train') as scope4:
    train = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

predicted = tf.cast(hypo > 0.5, dtype=tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))
accuracy_summ = tf.summary.scalar('accuracy', accuracy)

f = {X: x_data, Y: y_data}

with tf.Session() as sess:
    merged_summary = tf.summary.merge_all()
    writer = tf.summary.FileWriter("./xor_log/xor_logs_r0_01")
    writer.add_graph(sess.graph)  # Show the graph

    sess.run(tf.global_variables_initializer())

    for step in range(1001):
        summary, _ = sess.run([merged_summary, train], feed_dict=f)
        writer.add_summary(summary, global_step=step)

        if step % 100 == 0:
            print(step)
