if __name__ == "__main__":
    import tensorflow as tf
    import matplotlib.pyplot as plt
    import numpy as np
    from IPython import embed

    def qualikiz_sigmoid(x, name=""):
        dtype = x.dtype.name
        if tf.executing_eagerly():
            # return tf.divide(tf.constant(2, dtype),
            # tf.add(tf.constant(1, dtype),
            # tf.exp(tf.multiply(tf.constant(-2, dtype), x)))) - tf.constant(1, dtype)
            return "Eager stuff"
        else:
            return "Graph stuff"

    x = np.linspace(-2, 2, 50)
    plt.figure()
    plt.plot(x, tf.nn.relu(x).numpy(), label="relu")
    # plt.plot(x, tf.nn.relu6(x).numpy(), label='relu6')
    plt.plot(x, tf.nn.elu(x).numpy(), ".", label="elu")
    plt.plot(x, tf.nn.softplus(x).numpy(), label="softplus")
    plt.plot(x, tf.nn.softsign(x).numpy(), label="softsign")
    plt.plot(x, tf.nn.sigmoid(x).numpy(), label="sigmoid")
    plt.plot(x, tf.nn.tanh(x).numpy(), label="tanh")
    plt.plot(x, qualikiz_sigmoid(x).numpy(), label="QuaLiKiz")
    plt.legend()
    # plt.show()
