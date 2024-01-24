from tensorflow.keras.utils import to_categorical
from keras import backend as K
from keras.models import Sequential, load_model
from keras.layers import Conv1D, MaxPooling1D, BatchNormalization
from keras.layers.core import Activation, Flatten, Dense, Dropout
from keras.initializers import glorot_uniform
from keras.callbacks import ModelCheckpoint, EarlyStopping
import tensorflow as tf
import random
from keras.utils import np_utils
from keras.optimizers import Adamax
import numpy as np
import sys
import os
from timeit import default_timer as timer
from pprint import pprint
import argparse
import json
from sklearn.model_selection import train_test_split, StratifiedKFold
import sys

# Check if there are enough arguments
if len(sys.argv) < 2:
    print("Please provide an argument.")
    sys.exit(1)

argument = sys.argv[1]
#print(f"You provided the argument: {argument}")
np.random.seed(0)
random.seed(0)


# define the ConvNet
class ConvNet:
    @staticmethod
    def build(classes,
              input_shape,
              activation_function=("elu", "relu", "relu", "relu", "relu", "relu"),
              dropout=(0.1, 0.1, 0.1, 0.1, 0.5, 0.7),
              filter_num=(32, 64, 128, 256),
              kernel_size=8,
              conv_stride_size=1,
              pool_stride_size=4,
              pool_size=8,
              fc_layer_size=(512, 512)):

        # confirm that parameter vectors are acceptable lengths
        assert len(filter_num) + len(fc_layer_size) <= len(activation_function)
        assert len(filter_num) + len(fc_layer_size) <= len(dropout)

        # Sequential Keras model template
        model = Sequential()

        # add convolutional layer blocks
        for block_no in range(0, len(filter_num)):
            if block_no == 0:
                model.add(Conv1D(filters=filter_num[block_no],
                                 kernel_size=kernel_size,
                                 input_shape=input_shape,
                                 strides=conv_stride_size,
                                 padding='same',
                                 name='block{}_conv1'.format(block_no)))
            else:
                model.add(Conv1D(filters=filter_num[block_no],
                                 kernel_size=kernel_size,
                                 strides=conv_stride_size,
                                 padding='same',
                                 name='block{}_conv1'.format(block_no)))

            model.add(BatchNormalization())

            model.add(Activation(activation_function[block_no], name='block{}_act1'.format(block_no)))

            model.add(Conv1D(filters=filter_num[block_no],
                             kernel_size=kernel_size,
                             strides=conv_stride_size,
                             padding='same',
                             name='block{}_conv2'.format(block_no)))

            model.add(BatchNormalization())

            model.add(Activation(activation_function[block_no], name='block{}_act2'.format(block_no)))

            model.add(MaxPooling1D(pool_size=pool_size,
                                   strides=pool_stride_size,
                                   padding='same',
                                   name='block{}_pool'.format(block_no)))

            model.add(Dropout(dropout[block_no], name='block{}_dropout'.format(block_no)))

        # flatten output before fc layers
        model.add(Flatten(name='flatten'))

        # add fully-connected layers
        for layer_no in range(0, len(fc_layer_size)):
            model.add(Dense(fc_layer_size[layer_no],
                            kernel_initializer=glorot_uniform(seed=0),
                            name='fc{}'.format(layer_no)))

            model.add(BatchNormalization())
            model.add(Activation(activation_function[len(filter_num)+layer_no],
                                 name='fc{}_act'.format(layer_no)))

            model.add(Dropout(dropout[len(filter_num)+layer_no],
                              name='fc{}_drop'.format(layer_no)))

        # add final classification layer
        model.add(Dense(classes, kernel_initializer=glorot_uniform(seed=0), name='fc_final'))
        model.add(Activation('softmax', name="softmax"))

        # compile model with Adamax optimizer
        optimizer = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        model.compile(loss="categorical_crossentropy",
                      optimizer=optimizer,
                      metrics=["accuracy"])
        return model


def attack(X_train, y_train, X_valid, y_valid, X_test, y_test, num_classes, len_inp, VERBOSE=1):
    """
    """
    # convert class vectors to binary class matrices
    #classes = len(set(list(y_train)))
    #y_train = np_utils.to_categorical(y_train, classes)
    #y_valid = np_utils.to_categorical(y_valid, classes)
    #y_test = np_utils.to_categorical(y_test, classes)

    # # # # # # # # 
    # Build and compile model
    # # # # # # # # 
    print("Compiling model...")
    model = ConvNet.build(classes=num_classes, input_shape=(len_inp, 1))

    # # # # # # # # 
    # Train the model
    # # # # # # # # 
    filepath = 'model_fiber_data.h5'
    #checkpoint = ModelCheckpoint(filepath, monitor='val_loss', save_best_only=True, mode='max')
    #early_stopping = EarlyStopping(monitor='val_loss', patience=6, mode='auto', restore_best_weights=True)
    #callbacks_list = [checkpoint, early_stopping]

    #history = model.fit(X_train, y_train,
    #                    epochs=40,
    #                    verbose=VERBOSE,
    #                    validation_data=(X_valid, y_valid),
    #                    callbacks=callbacks_list)

    # Save & reload model
    #model.save(filepath)
    #del model
    model = load_model(filepath)

    # # # # # # # # 
    # Test the model
    # # # # # # # # 
    score = model.evaluate(X_test, y_test,
                           verbose=VERBOSE)
    score_train = model.evaluate(X_train, y_train,
                                 verbose=VERBOSE)

    # # # # # # # # 
    # Print results
    # # # # # # # # 
    print("\n=> Train score:", score_train[0])
    print("=> Train accuracy:", score_train[1])

    print("\n=> Test score:", score[0])
    print("=> Test accuracy:", score[1])

    return score[1]


def main():
    """
    """
    len_inp = int(argument)
    inputShape = (len_inp,1)
    num_classes = 75   # adjust to match your data

    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

    if tf.test.gpu_device_name():
        print('GPU found')
    else:
        print("No GPU found")

    x = np.load('X_satlink_data.npy')
    y = np.load('Y_satlink_data.npy')

    permutation = np.random.permutation(len(x))  # Generate a random index permutation
    x = x[permutation]  # Index both arrays with the same permutation
    y = y[permutation]
    X = np.empty((6000,len_inp,1))
    for i in range(len(X)):
        X[i] = np.reshape(x[i], (len_inp, 1))
    print(X.shape)
    print(y.shape)
    print(min(y))
    print(max(y))

    # Initialize StratifiedKFold
    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)

    res = []

    # Perform 10-fold stratified cross-validation on the entire dataset
    for train_val_index, test_index in skf.split(X, y):
        X_train_val, X_test = X[train_val_index], X[test_index]
        y_train_val, y_test = y[train_val_index], y[test_index]
        
        # Split the train_val set into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=1/9, stratify=y_train_val, random_state=0)
        
        print("TRAIN:", len(X_train), "VAL:", len(X_val), "TEST:", len(X_test))

        Y_train = to_categorical(y_train, num_classes)
        Y_test = to_categorical(y_test, num_classes)
        Y_val = to_categorical(y_val, num_classes)

        print(X_train.shape)
        print(Y_train.shape)
        print(X_val.shape)
        print(Y_val.shape)
        print(X_test.shape)
        print(Y_test.shape)
        print(X_train[100][0:10])
        print(y_train[100])
        print(np.sort(y_test))
        print(np.sort(y_val))

        acc = attack(X_train, Y_train, X_val, Y_val, X_test, Y_test, num_classes, len_inp, VERBOSE=1)
        res.append(acc)

    

    print("======================")
    print("-- Summary")
    print("======================")
    print(res)
    sum = 0
    for i in range(len(res)):
        sum = sum + res[i]
    print(sum/len(res))

if __name__ == "__main__":
    # execute only if run as a script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)

