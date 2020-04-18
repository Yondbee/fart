import tensorflow as tf

import IPython.display as display

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (12,12)
mpl.rcParams['axes.grid'] = False

import numpy as np
import PIL.Image
import time
import functools

def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)

#content_path = tf.keras.utils.get_file('YellowLabradorLooking_new.jpg', 'https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg')
#content_path = tf.keras.utils.get_file('gorilla.jpg', 'https://wallpapermemory.com/uploads/427/gorilla-wallpaper-hd-1920x1080-145603.jpg')
#content_path = tf.keras.utils.get_file('baloo.jpg', 'https://scontent-mad1-1.cdninstagram.com/v/t51.2885-15/e35/14562053_1069598309828588_4501745636017700864_n.jpg?_nc_ht=scontent-mad1-1.cdninstagram.com&_nc_cat=108&_nc_ohc=wpMpw7G-3FEAX_WYwla&oh=d6be6a42f6cf5a48dcc9f7855780df81&oe=5EBE1987')
content_path = tf.keras.utils.get_file('park.jpg', 'https://es.parisinfo.com/var/otcp/sites/images/media/1.-photos/01.-ambiance-630-x-405/parc-des-buttes-chaumont-630x405-c-otcp-david-lefranc-158-32/23920-1-fre-FR/Parc-des-Buttes-Chaumont-630x405-C-OTCP-David-Lefranc-158-32.jpg')



# https://commons.wikimedia.org/wiki/File:Vassily_Kandinsky,_1913_-_Composition_7.jpg
#style_path = tf.keras.utils.get_file('kandinsky5.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg')
#style_path = tf.keras.utils.get_file('hopper_corner.jpg','https://www.nga.gov/content/dam/ngaweb/features/slideshows/edward-hopper/hopper_corner.jpg')
#style_path = tf.keras.utils.get_file('vgrhone.jpg','https://i.etsystatic.com/9089439/r/il/2befad/1671747429/il_1588xN.1671747429_m2m9.jpg')
#style_path = tf.keras.utils.get_file('vgcorn.jpg','https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Vincent_Van_Gogh_-_Wheatfield_with_Crows.jpg/2880px-Vincent_Van_Gogh_-_Wheatfield_with_Crows.jpg')
style_path = tf.keras.utils.get_file('vgthunder.jpg','https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Vincent_van_Gogh_-_Wheatfield_Under_Thunderclouds_-_VGM_F778.jpg/2880px-Vincent_van_Gogh_-_Wheatfield_Under_Thunderclouds_-_VGM_F778.jpg')




def load_img(path_to_img, max_dim = 256):
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img

def imshow(image, title=None):
  if len(image.shape) > 3:
    image = tf.squeeze(image, axis=0)

  plt.imshow(image)
  if title:
    plt.title(title)
    
content_image = load_img(content_path, 1024)
style_image = load_img(style_path, 512)

#content_image = load_img('./audrey.jpg');
#style_image = load_img('./La maja desnuda.jpg');


plt.subplot(3, 1, 1)
imshow(content_image, 'Content Image')

plt.subplot(3, 1, 2)
imshow(style_image, 'Style Image')

import tensorflow_hub as hub
hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
stylized_image = hub_module(tf.constant(content_image), tf.constant(style_image))[0]

plt.subplot(3, 1, 3)
stylized = tensor_to_image(stylized_image)
plt.imshow(np.asarray(stylized))
plt.title('Stylized Image')

stylized.save('baloo-kandynsky.jpg')

plt.waitforbuttonpress()