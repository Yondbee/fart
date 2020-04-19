import tensorflow as tf
with tf.device('/cpu:0'):
    a_c = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a-cpu')
    b_c = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b-cpu')
    print tf.matmul(a_c, b_c, name='c-cpu')

if tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None):
    with tf.device('/gpu:0'):
        a_g = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a-gpu')
        b_g = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b-gpu')
        print tf.matmul(a_g, b_g, name='c-gpu')

print tf.config.list_physical_devices('GPU')