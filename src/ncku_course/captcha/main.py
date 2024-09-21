import tensorflow as tf
from tensorflow.keras import layers, Model # type: ignore
from tensorflow.keras.backend import ctc_batch_cost, ctc_decode # type: ignore
from pathlib import Path
from tensorflow.data.experimental import AUTOTUNE # type: ignore
import matplotlib.pyplot as plt
from tensorflow.python.data.ops.from_tensor_slices_op import _TensorSliceDataset
from tensorflow.python.data.ops.dataset_ops import DatasetV2
from typing import List, Tuple, Union
from tensorflow.keras import backend # type: ignore
import os



#---------------args config-----------------
#possible chars set
char_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z']

#data path for training
data_dir = r"C:\Users\user\OneDrive\documents\code\Python\Projects\captcha\source"

#excepted image size
img_width = 400
img_height = 50

max_label_length = 8
batch_size = 16
num_epochs = 30
#-------------------------------------------

char_set_len = len(char_set)
char_to_int = {char: i for i, char in enumerate(char_set)}
int_to_char = {i: char for char, i in char_to_int.items()}
extract_label = lambda path: path.split('_')[0]
current_dir = os.path.dirname(os.path.abspath(__file__))

# CTC loss function
def ctc_loss(y_true, y_pred):
    input_length = tf.fill((batch_size, 1), tf.shape(y_pred)[1])
    label_length = tf.fill((batch_size, 1), max_label_length)
    loss = ctc_batch_cost(y_true, y_pred, input_length, label_length)
    return loss

#process img to tensor style
def preprocess_image(image_path, add_batch_dim=False):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=1)
    image = tf.image.resize(image, (img_height, img_width))
    if add_batch_dim:
        image = tf.expand_dims(image, axis=0)
    return image

#check label length if exceed max label length
def check_label_length(dataset):
    for _, labels in dataset:
        for label in labels:
            if len(label) > max_label_length:
                raise Exception(f"Label length {len(label)} exceeds max label length {max_label_length}")

def get_image_paths(data_dir) -> Tuple[List[str], int]:
    image_paths = [str(image) for image in sorted(Path(data_dir).glob("*.jpg"))]
    
    return image_paths, len(image_paths)

def prepare_data(data_dir : str, batch_size : int, training_data_ratio : float = 0.8) -> Tuple[DatasetV2, DatasetV2]:
    image_paths, _ = get_image_paths(data_dir)
    labels = [extract_label(image.stem) for image in sorted(Path(data_dir).glob("*.jpg"))]

    images = [preprocess_image(image_path) for image_path in image_paths]
    encoded_labels : List[List[int]] = [[char_to_int[char] for char in label] for label in labels]

    # 構建tf.data數據集
    dataset : _TensorSliceDataset = tf.data.Dataset.from_tensor_slices((images, encoded_labels))

    dataset = dataset.shuffle(buffer_size=len(images))

    # Split the dataset into training and validation sets (adjust as needed)
    train_size = int(training_data_ratio * len(image_paths))
    train_dataset = dataset.take(train_size).batch(batch_size).prefetch(buffer_size=AUTOTUNE)
    validation_dataset = dataset.skip(train_size).batch(batch_size).prefetch(buffer_size=AUTOTUNE)
    check_label_length(train_dataset)
    check_label_length(validation_dataset)
    
    return train_dataset, validation_dataset

def build_model():
    # define the input shape
    input_data = layers.Input(shape=(img_height, img_width, 1), name='image')
    
    #standardize the input
    x = layers.Rescaling(1./255)(input_data)
    
    #Transpose the tensor to shape (None, image_width, image_height, 1)
    x = layers.Lambda(lambda x: tf.transpose(x, perm=[0, 2, 1, 3]), name="transpose")(x)
    
    #conv layer 1
    x = layers.Conv2D(32, (3, 3), activation='relu', 
                      kernel_initializer='he_normal', padding='same', name='Conv1')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), name='pool1')(x)

    #conv layer 2
    x = layers.Conv2D(64, (3, 3), activation='relu', 
                      kernel_initializer='he_normal', padding='same', name='Conv2')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), name='pool2')(x)

    #conv layer 3
    x = layers.Conv2D(128, (3, 3), activation='relu', 
                      kernel_initializer='he_normal', padding='same', name='Conv3')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 1), name='pool3')(x)

    #adjust the shape to fit bidirectional LSTM
    new_shape = ((img_width // 8), (img_height // 4) * 128)
    x = layers.Reshape(target_shape=new_shape, name="reshape")(x)
    x = layers.Dense(128, activation='relu', name="dense1")(x)
    x = layers.Dropout(0.2)(x)

    #bidirectional LSTM layer
    x = layers.Bidirectional(layers.LSTM(128, return_sequences=True, dropout=0.25))(x)
    
    #output layer
    output = layers.Dense(char_set_len + 1, activation="softmax", name="dense2")(x)
    
    model = Model(input_data, output, name = 'model')
    
    model.compile(loss=ctc_loss, optimizer='adam')
    
    return model

def visualize_sample(image, label):
    plt.figure(figsize=(8, 2))
    plt.imshow(image[:, :, 0], cmap='gray')
    plt.title("Label: " + ''.join(label), fontsize=18)
    plt.axis('off')
    plt.show()

def visualize_random_samples(dataset, int_to_char, num_samples=5):
    # Create an iterator for the dataset
    dataset_iter = iter(dataset)

    # Iterate through the random samples and visualize them
    for _ in range(num_samples):
        image, label = next(dataset_iter)

        # Decode the label (convert integers to characters)
        label = [int_to_char[int(x)] for x in label[0].numpy()]

        # Display the image and label
        visualize_sample(image[0], label)

def start_training(train_dataset, validation_dataset, num_epochs):
    model = build_model()
    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='loss',
            patience=5,
            verbose=1,
            restore_best_weights=True),
    ]

    history = model.fit(
        train_dataset,
        epochs=num_epochs,
        validation_data=validation_dataset,
        callbacks=callbacks
    )
    
    return model, history

# train_dataset, validation_dataset = prepare_data(data_dir, batch_size)
# visualize_random_samples(validation_dataset, int_to_char, num_samples=2)

#start training
# model, history = start_training(train_dataset, validation_dataset, num_epochs)

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

def decode_and_visualize_samples(model, dataset, int_to_char, num_batchs : int = 5, max_figs_showed : int = 100):
    t, f = 0, 0

    dataset_iter = iter(dataset)

    for _ in range(num_batchs):
        images, origin_labels = next(dataset_iter)
        predictions = model.predict(images, verbose=0)
        decoded_dense = decode(predictions)
            
        for i in range(len(decoded_dense[0])):
            image, origin_label, decoded = images[i], origin_labels[i], decoded_dense[0][i]
            origin_label = ''.join([int_to_char[int(x)]  for x in origin_label[:max_label_length].numpy()])
            decoded_label = ''.join([int_to_char[int(x)] if int(x) != -1 else '' for x in decoded[:max_label_length].numpy()])
            
            if origin_label != decoded_label:
                f += 1
            else:
                t += 1
            
            if t + f <= max_figs_showed:    
                visualize_sample(image, decoded_label)
            
    if t + f == 0:
        print("No samples")
    print(f"Total samples: {t + f}, correct: {t}, failed: {f}\naccuracy: {t/(t + f):.2f}")

def decode_single_sample(model, path : str, int_to_char) -> str:
    image = preprocess_image(path, add_batch_dim=True)
    predictions = model.predict(image, verbose=0)
    decoded_dense = decode(predictions)
    decoded = decoded_dense[0][0]
    decoded_label = ''.join([int_to_char[int(x)] if int(x) != -1 else '' for x in decoded[:max_label_length].numpy()])

    return decoded_label

def test_model(model, test_data_path, int_to_char):
    test_dataset = prepare_data(test_data_path, batch_size, 1)[0]
    _, total_num = get_image_paths(test_data_path)
    print(total_num)
    decode_and_visualize_samples(model, test_dataset, int_to_char, total_num // 16 if total_num >= 16 else 1) 
    
# test_path = r"C:\Users\user\OneDrive\documents\code\Python\Projects\captcha\test_source"
# test_model(model, data_dir, int_to_char)
import time

start = time.time()
#load trained model
model = tf.keras.models.load_model(current_dir + '/model_20240828_2152', custom_objects={'ctc_loss': ctc_loss})
pred_label = decode_single_sample(model, r"C:\Users\user\OneDrive\documents\code\Python\Projects\captcha\data\gpwkmnwm\gpwkmnwm_1.jpg", int_to_char)
print(pred_label)
print(time.time() - start)
# model.save('./model_20240828_2152.h5')