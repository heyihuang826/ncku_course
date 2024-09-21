import tensorflow as tf
from tensorflow.keras.backend import ctc_batch_cost # type: ignore
from typing import List, Tuple, Union
from tensorflow.keras import backend # type: ignore



#possible chars set
char_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z']

#excepted image size
img_width = 400
img_height = 50

max_label_length = 8
batch_size = 16

char_to_int = {char: i for i, char in enumerate(char_set)}
int_to_char = {i: char for char, i in char_to_int.items()}

# CTC loss function
def ctc_loss(y_true, y_pred):
    input_length = tf.fill((batch_size, 1), tf.shape(y_pred)[1])
    label_length = tf.fill((batch_size, 1), max_label_length)
    loss = ctc_batch_cost(y_true, y_pred, input_length, label_length)
    return loss

#process img to tensor style
def preprocess_image(image, add_batch_dim=False):
    if type(image) == str: #path
        image = tf.io.read_file(image)
        image = tf.image.decode_jpeg(image, channels=1)
    else: #content
        image = tf.io.decode_image(image, channels=1)
    
    image = tf.image.resize(image, (img_height, img_width))
    if add_batch_dim:
        image = tf.expand_dims(image, axis=0)
    return image

def decode(predictions):
    input_shape = tf.shape(predictions)
    num_samples, num_steps = input_shape[0], input_shape[1]
    new_shape = tf.fill((num_samples, ), num_steps)
    predictions = tf.math.log(
    tf.transpose(predictions, perm=[1, 0, 2]) + backend.epsilon()
        )
    decoded, _ = tf.nn.ctc_greedy_decoder(predictions, sequence_length=new_shape)
    
    decoded_dense = []
    for st in decoded:
        st = tf.SparseTensor(st.indices, st.values, (num_samples, num_steps))
        decoded_dense.append(tf.sparse.to_dense(sp_input=st, default_value=-1))
        
    return decoded_dense

def decode_single_sample(model, data, int_to_char) -> str:
    image = preprocess_image(data, add_batch_dim=True)
    predictions = model.predict(image, verbose=0)
    decoded_dense = decode(predictions)
    decoded = decoded_dense[0][0]
    decoded_label = ''.join([int_to_char[int(x)] if int(x) != -1 else '' for x in decoded[:max_label_length].numpy()])

    return decoded_label

# import time

# start = time.time()
# #load trained model
# model = tf.keras.models.load_model('./model_20240828_2152', custom_objects={'ctc_loss': ctc_loss})
# pred_label = decode_single_sample(model, r"C:\Users\user\OneDrive\documents\code\Python\Projects\captcha\data\gpwkmnwm\gpwkmnwm_1.jpg", int_to_char)
# print(pred_label)
# print(time.time() - start)