from vgg import vgg_16
import tensorflow as tf
import tensorflow.contrib.slim as slim

NUM_BOXES = 5


def ssd(inputs, num_class = 1, training=True):
    _, net = vgg_16(inputs, num_classes=0, is_training=training, spatial_squeeze=False)

    inputs = net["vgg_16/conv5/conv5_3"]
    transfer_layers = []
    transfer_layers.append(net["vgg_16/conv4/conv4_3"])

    with tf.variable_scope("fc_layers"):
        inputs = slim.conv2d(inputs, 1024, [3, 3], padding="same", scope="fc6")
        inputs = slim.conv2d(inputs, 1024, [1, 1], padding="same", scope="fc7")
        transfer_layers.append(inputs)

    with tf.variable_scope("ssd_layers"):
        inputs = slim.conv2d(inputs, 256, [1,1], 1, activation_fn=tf.nn.relu, padding="same", scope="conv8_1")
        inputs = slim.conv2d(inputs, 512, [3,3], 2, activation_fn=tf.nn.relu, padding="same", scope="conv8_2")
        transfer_layers.append(inputs)

        inputs = slim.conv2d(inputs, 128, [1,1], 1, activation_fn=tf.nn.relu, padding="same", scope="conv9_1")
        inputs = slim.conv2d(inputs, 256, [3,3], 2, activation_fn=tf.nn.relu, padding="same", scope="conv9_2")
        transfer_layers.append(inputs)

        inputs = slim.conv2d(inputs, 128, [1,1], 1, activation_fn=tf.nn.relu, padding="same", scope="conv10_1")
        inputs = slim.conv2d(inputs, 256, [3,3], 2, activation_fn=tf.nn.relu, padding="same", scope="conv10_2")
        transfer_layers.append(inputs)

        # inputs = slim.conv2d(inputs, 128, [1,1], 1, activation_fn=tf.nn.relu, padding="valid", scope="conv11_1")
        # inputs = slim.conv2d(inputs, 256, [3,3], 1, activation_fn=tf.nn.relu, padding="valid", scope="conv11_2")
        # transfer_layers.append(inputs)

    with tf.variable_scope("outputs"):
        # TODO: Add l2 norm before fist output
        # REF: https://medium.com/@smallfishbigsea/understand-ssd-and-implement-your-own-caa3232cd6ad
        # L2 norm: http://mathworld.wolfram.com/L2-Norm.html
        outputs = []
        for tl in transfer_layers:
            # TODO: Add varying number of boxes
            result = slim.conv2d(tl, (num_class + 4) * NUM_BOXES, [3, 3])
            outputs.append(result)

    print(outputs)

    return outputs


def ssd_acc_loss():
    # TODO: Implement accuracy loss
    pass


def ssd_loc_loss():
    # TODO: Implement location loss
    pass


def ssd_total_loss():
    # TODO: Implement total loss
    pass


def decode_output():
    # TODO: Implement output decoding
    pass
    

# Testing
placeholder = tf.placeholder(tf.float32, (1, 300, 300, 3), "inputs")
net = ssd(placeholder)