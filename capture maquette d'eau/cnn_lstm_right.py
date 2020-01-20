from __future__ import print_function
import time

start = time.time()
from matplotlib import pyplot
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import MaxPooling1D, Conv1D, TimeDistributed, Activation, Flatten
import pandas as pd
from sklearn.preprocessing import Normalizer
from keras.layers import Dense,Dropout
import numpy as np
from keras.layers import LSTM


data = pd.read_table('Capture Data/right_lstm_raspi_data_grosse.txt', delimiter=",", header=None)

# Conversion from hexa to int when needed...
def to_decimal(data, listofindexestobechanged):
    for index in listofindexestobechanged:
        liste = []
        for value in data.iloc[:, index]:
            liste.append(int(value, base=16))
        data.iloc[:, index] = liste
    return data


data = to_decimal(data, [2])

# =======

X = data.iloc[:, 0:-1]
y = data.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=0)

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

#Model definition

cnn_lstm = Sequential()
cnn_lstm.add(Conv1D(64, 3, activation="relu", input_shape=(13, 1), padding="same"))
cnn_lstm.add(MaxPooling1D(pool_length=2))
cnn_lstm.add(LSTM(300, return_sequences=True))
cnn_lstm.add(Dropout(0.1)) #Avoid overfitting in the model
cnn_lstm.add(LSTM(300, return_sequences=True))
cnn_lstm.add(Flatten())
cnn_lstm.add(TimeDistributed(Dense(100)))
cnn_lstm.add(Activation('linear'))
cnn_lstm.add(Dense(1, activation="linear"))

print(cnn_lstm.summary())

cnn_lstm.compile(loss="mean_absolute_error", optimizer="adam", metrics=['mae'])

# train
history = cnn_lstm.fit(X_train, y_train, epochs=100, batch_size=8, verbose = 0)

scores = cnn_lstm.evaluate(X_val, y_val, verbose=1)
print("%s: %.2f" % (cnn_lstm.metrics_names[1], scores[1]))

running_time = time.time() - start
print("Total running time : ", running_time)

plot = True
if plot:
    pyplot.plot(history.history['mae'], "-r", label="Mean Absolute Error")
    pyplot.legend(loc="upper right")

    pyplot.xlabel("Epochs")
    pyplot.title("Evolution of the Mean Absolute Error (LSTM)")
    pyplot.show()


cnn_lstm.save("cnn_lstm_model_right.hdf5")