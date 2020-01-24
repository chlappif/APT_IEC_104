from __future__ import print_function
import time

from tensorflow import keras

start = time.time()

from matplotlib import pyplot
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Conv1D, Activation, Flatten
import pandas as pd
from sklearn.preprocessing import Normalizer
from keras.layers import Dense, Dropout
import numpy as np
from keras.layers import LSTM


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

# ========== PART 1 ============#
# Datasets construction

if make_datasets:
    data = pd.read_table('Capture Data/left_raspi_data_grosse.txt', delimiter=",", header=None)

    # Conversion from hexa to int when needed...
    def to_decimal(data, listofindexestobechanged):
        for index in listofindexestobechanged:
            liste = []
            for value in data.iloc[:, index]:
                liste.append(int(value, base=16))
            data.iloc[:, index] = liste
        return data

    data = to_decimal(data, [1])

    X = data.iloc[:, 0:-1]
    y = data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=0)

# ========== PART 2 ============ #

if make_model:
    scaler = Normalizer().fit(X_train)
    X_train = scaler.transform(X_train)
    scaler_v = Normalizer().fit(X_val)
    X_val = scaler_v.transform(X_val)
    scaler_t = Normalizer().fit(X_test)
    X_test = scaler_t.transform(X_test)
    print(X_train.shape, X_val.shape, X_test.shape)

    # reshape input to be [samples, time steps, features]
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    X_val = np.reshape(X_val, (X_val.shape[0], X_val.shape[1], 1))
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    lstm_output_size = 70
    look_back = 5

    # Model definition
    cnn_lstm = Sequential()
    cnn_lstm.add(Conv1D(64, 3, activation="relu", input_shape=(12, 1), padding="same"))
    # cnn_lstm.add(MaxPooling1D(pool_length=2))
    cnn_lstm.add(LSTM(64, return_sequences=True))
    cnn_lstm.add(Dropout(0.5))  # Avoid overfitting in the model
    cnn_lstm.add(Flatten())
    cnn_lstm.add(Dense(64, activation="relu"))
    cnn_lstm.add(Activation('linear'))
    cnn_lstm.add(Dense(1, activation="linear"))

    print(cnn_lstm.summary())

    if learn:
        cnn_lstm.compile(loss="mean_absolute_error", optimizer="adam", metrics=['mae'])

        # train
        history = cnn_lstm.fit(X_train, y_train, epochs=150, batch_size=8, verbose=0)

        scores = cnn_lstm.evaluate(X_val, y_val, verbose=1)
        print("%s: %.2f" % (cnn_lstm.metrics_names[1], scores[1]))

        running_time = time.time() - start
        print("Total running time : ", running_time)

        # ========== PART 3 ============#

        if plot:
            pyplot.plot(history.history['mae'], "-r", label="Mean Absolute Error")
            pyplot.legend(loc="upper right")
            pyplot.xlabel("Epochs")
            pyplot.title("Evolution of the Mean Absolute Error (LSTM)")
            pyplot.show()

        cnn_lstm.save("cnn_lstm_model_left.hdf5")

# ========== PART 4 ============#

if test_model:
    cnn_lstm.load_weights("cnn_lstm_model_left.hdf5")
    y_pred = cnn_lstm.predict(X_test)
    mae = keras.losses.mean_absolute_error(y_test, y_pred)

    print("Mean Absolute Error : ", "%.5f (+/- %.5f)" % (np.mean(mae), np.std(mae)))

    yy = []
    for elem in y_test:
        yy.append([elem])
    pyplot.plot(yy[1:200], '-r', label="Reality", marker="*")
    pyplot.plot(y_pred[:200], '-g', label="Prediction", marker="x")
    pyplot.ylabel("Water level in the left tank (cm)")
    pyplot.legend(loc="upper right")
    pyplot.title("Comparison between water level predictions and reality (CNN+LSTM)")
    pyplot.show()
