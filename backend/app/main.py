# Copyright 2019 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Flask config
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

import tensorflow as tf

import numpy as np
import PIL.Image
import time
import functools
import os
from io import BytesIO


import tensorflow_hub as hub
hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

from flask import Flask, send_file, request
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)

def load_img(path_to_img, max_dim = None):
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    if max_dim != None:
        shape = tf.cast(tf.shape(img)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        img = tf.image.resize(img, new_shape)
    
    img = img[tf.newaxis, :]

    return img

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=85)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fartist', methods=['POST'])
def fartist():

    if 'src' not in request.files or 'sty' not in request.files:
        return 'Specify src and sty', 400

    src = file = request.files['src']
    sty = file = request.files['sty']

    if src.filename == '' or sty.filename == '':
        return 'Specify src and sty', 400

    if not allowed_file(src.filename):
        return 'Src file extension not admitted', 400

    if not allowed_file(sty.filename):
        return 'Sty extension not admitted', 400

    #content_path = tf.keras.utils.get_file('park.jpg', 'https://es.parisinfo.com/var/otcp/sites/images/media/1.-photos/01.-ambiance-630-x-405/parc-des-buttes-chaumont-630x405-c-otcp-david-lefranc-158-32/23920-1-fre-FR/Parc-des-Buttes-Chaumont-630x405-C-OTCP-David-Lefranc-158-32.jpg')
    #style_path = tf.keras.utils.get_file('vgthunder.jpg','https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Vincent_van_Gogh_-_Wheatfield_Under_Thunderclouds_-_VGM_F778.jpg/2880px-Vincent_van_Gogh_-_Wheatfield_Under_Thunderclouds_-_VGM_F778.jpg')

    content_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(src.filename))
    content_image = load_img(content_path)

    style_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(sty.filename))
    style_image = load_img(style_path, 512)
    
    stylized_image_tensor = hub_module(tf.constant(content_image), tf.constant(style_image))[0]
    stylized_image = tensor_to_image(stylized_image_tensor)
    return serve_pil_image(stylized_image)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)