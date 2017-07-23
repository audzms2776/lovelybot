import numpy as np
import tensorflow as tf

num_points = 10000
vector_set = []

for i in range(num_points):
    x1 = np.random.normal(0.0, 0.55)
    y1 = x1 * 0.1 + 0.3 + np.random.normal(0.0, 0.03)
    vector_set.append([x1, y1])

x_data = [v[0] for v in vector_set]
y_data = [v[1] for v in vector_set]

X = tf.placeholder(tf.float32, shape=[None], name='x-input')
Y = tf.placeholder(tf.float32, shape=[None], name='y-input')

W = tf.Variable(tf.random_normal([1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')

tf.summary.histogram('weight', W)
tf.summary.histogram('bias', b)

hypo = X * W + b
tf.summary.histogram('hypo', hypo)

cost = tf.reduce_mean(tf.square(hypo - Y))
tf.summary.scalar('cost', cost)

train = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
merged_summary = tf.summary.merge_all()
writer = tf.summary.FileWriter("./linear_log/linear")
writer.add_graph(sess.graph)  # Show the graph

for step in range(2000):
    summary, cost_val, W_val, b_val, _ = sess.run([merged_summary, cost, W, b, train], feed_dict={X: x_data, Y: y_data})
    writer.add_summary(summary, global_step=step)
    if step % 20 == 0:
        print(step, cost_val, W_val, b_val)
