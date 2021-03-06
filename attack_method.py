import numpy as np
import tensorflow as tf
from utils import *

def n_staircase_sign(noise, n):
    noise_staircase = tf.zeros(shape=noise.shape)
    medium = []
    sign = tf.sign(noise)
    temp_noise = noise
    abs_noise = abs(noise)
    base = n / 100
    for i in np.arange(n, 100.1, n):
        medium_now = tf.contrib.distributions.percentile(abs_noise, q = i, axis = [1,2], keep_dims = True, interpolation='lower')
        medium.append(medium_now)
    for j in range(len(medium)):
        update = sign * tf.cast(abs(temp_noise) <= medium[j], tf.float32) * (base + 2 * base * j)
        noise_staircase += update
        temp_noise += update * 1e5

    return noise_staircase



def gkern(kernlen=21, nsig=3):
  """Returns a 2D Gaussian kernel array."""
  import scipy.stats as st

  x = np.linspace(-nsig, nsig, kernlen)
  kern1d = st.norm.pdf(x)
  kernel_raw = np.outer(kern1d, kern1d)
  kernel = kernel_raw / kernel_raw.sum()
  kernel = kernel.astype(np.float32)
  stack_kernel = np.stack([kernel, kernel, kernel]).swapaxes(2, 0)
  stack_kernel = np.expand_dims(stack_kernel, 3)
  return stack_kernel


def input_diversity(FLAGS, input_tensor):
    rnd = tf.random_uniform((), FLAGS.image_width, FLAGS.image_resize, dtype=tf.int32)
    rescaled = tf.image.resize_images(input_tensor, [rnd, rnd], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    h_rem = FLAGS.image_resize - rnd
    w_rem = FLAGS.image_resize - rnd
    pad_top = tf.random_uniform((), 0, h_rem, dtype=tf.int32)
    pad_bottom = h_rem - pad_top
    pad_left = tf.random_uniform((), 0, w_rem, dtype=tf.int32)
    pad_right = w_rem - pad_left
    padded = tf.pad(rescaled, [[0, 0], [pad_top, pad_bottom], [pad_left, pad_right], [0, 0]], constant_values=0.)
    padded.set_shape((input_tensor.shape[0], FLAGS.image_resize, FLAGS.image_resize, 3))
    return tf.cond(tf.random_uniform(shape=[1])[0] < tf.constant(FLAGS.prob), lambda: padded, lambda: input_tensor)


def project_kern(kern_size):
    kern = np.ones((kern_size, kern_size), dtype=np.float32) / (kern_size ** 2 - 1)
    kern[kern_size // 2, kern_size // 2] = 0.0
    kern = kern.astype(np.float32)
    stack_kern = np.stack([kern, kern, kern]).swapaxes(0, 2)
    stack_kern = np.expand_dims(stack_kern, 3)
    return stack_kern, kern_size // 2


def project_noise(x, stack_kern, kern_size):
    x = tf.pad(x, [[0,0],[kern_size,kern_size],[kern_size,kern_size],[0,0]], "CONSTANT")
    x = tf.nn.depthwise_conv2d(x, stack_kern, strides=[1, 1, 1, 1], padding='VALID')
    return x
