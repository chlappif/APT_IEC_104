from __future__ import print_function

import os
import numpy as np
import time
from matplotlib import pyplot
from tensorflow import keras

start_time = time.time()
seed = 7
from keras.models import Sequential
import pandas as pd

from sklearn.preprocessing import Normalizer
from keras.layers import Dense
# To divide data into subsets, and in order to use cross-validation
from sklearn.model_selection import train_test_split, StratifiedKFold


# THIS CODE WAS ONLY ADAPTED FROM THE RIGHT SIDE RPI : IT MIGHT NEED SOME DEBUGGING
# THERE MIGHT BE SOME ERRORS DUE TO FILE NAMES ISSUES FOR INSTANCE


# TO DO : change code so that the datasets are always the same version as the model
# => Prevent training on a set, testing on a different set but at second time
# => With this version, it is more accurate to always set every parameter to True (except Plot)

make_datasets = True
make_model = True  # To construct the model to be used in
learn = True
plot = True
test_model = True

# ========== PART 1 ============ #
# Datasets construction

if make_datasets:

    data = pd.read_table(os.fspath("./Capture Data/left_raspi_data_grosse.txt"), delimiter=",", header=None)


    # Conversion from hexa to int when needed...
    def to_decimal(data, listofindexestobechanged):
        for index in listofindexestobechanged:
            liste = []
            for value in data.iloc[:, index]:
                liste.append(int(value, base=16))
            data.iloc[:, index] = liste
        return data


    data = to_decimal(data, [1])

    # =======

    X = data.iloc[:, 0:-1]
    y = data.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# ========== PART 2 ============ #

if make_model:

    scaler_train = Normalizer().fit(X_train)  # Inutile ?
    X_train = scaler_train.transform(X_train)  # Normalisation des données
    scaler_test = Normalizer().fit(X_test)
    X_test = scaler_test.transform(X_test)

    y_train = np.array(y_train)
    y_test = np.array(y_test)
    # reshape input to be [samples, time steps, features]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1]))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1]))

    kfold = StratifiedKFold(n_splits=10, shuffle=True)

    model = Sequential()
    model.add(Dense(32, input_dim=12, activation='relu', kernel_initializer='he_uniform', use_bias=True))
    model.add(Dense(64, activation='relu', kernel_initializer='he_uniform', use_bias=True))
    model.add(Dense(128, activation='relu', kernel_initializer='he_uniform', use_bias=True))
    model.add(Dense(128, activation='relu', kernel_initializer='he_uniform', use_bias=True))
    model.add(Dense(128, activation='relu', kernel_initializer='he_uniform', use_bias=True))
    model.add(Dense(64, activation='relu', kernel_initializer='he_uniform', use_bias=True))
    model.add(Dense(32, activation='relu', kernel_initializer='he_uniform', use_bias=True))
    model.add(Dense(16, activation='relu', kernel_initializer='he_uniform', use_bias=True))
    model.add(Dense(1, input_shape=(16,), activation='linear', use_bias=True))

    print(model.summary())

    if learn:
        model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mae'])

        maes = []

        for train, val in kfold.split(X_train, y_train):
            # Fit the model
            history = model.fit(X_train[train], y_train[train], epochs=150, batch_size=8, verbose=0)
            # evaluate the model
            scores = model.evaluate(X_train[val], y_train[val], verbose=1)
            print("%s: %.2f" % (model.metrics_names[1], scores[1]))
            maes.append(scores[1])

            # ========== PART 3 ============ #
            # Code to be used only to print nice plots

            if plot:
                pyplot.plot(history.history['mae'], "-r", label="Mean Absolute Error")
                pyplot.legend(loc="upper right")

                pyplot.xlabel("Epochs")
                pyplot.title("Evolution of the Mean Absolute Error during the training on one fold")
                pyplot.show()

        model.save("fcn_model.hdf5")

        print("Averaged parameters : ")
        print("Mean Absolute Error : ", "%.5f (+/- %.5f)" % (np.mean(maes), np.std(maes)))

        interval = time.time() - start_time
        print('Total time in seconds:', interval)


# ========== PART 4 ============ #

if test_model:
    model.load_weights("fcn_model.hdf5")

    y_pred = model.predict(X_test)
    mae = keras.losses.mean_absolute_error(y_test, y_pred)

    print("Mean Absolute Error : ", "%.5f (+/- %.5f)" % (np.mean(mae), np.std(mae)))
    pyplot.plot(y_test[:200], '-r', label="Reality", marker='*')
    pyplot.plot(y_pred[:200], '-g', label="Prediction")
    pyplot.ylabel("Water level in the left tank (cm)")
    pyplot.legend(loc="upper right")
    pyplot.title("Comparison between water level predictions and reality (FFNN)")
    pyplot.show()
