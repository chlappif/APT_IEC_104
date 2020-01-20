from __future__ import print_function
import numpy as np
from sklearn.model_selection import train_test_split

np.random.seed(1337)  # for reproducibility


from keras.models import Sequential
from keras.layers import Convolution1D,MaxPooling1D
import pandas as pd
from sklearn.preprocessing import Normalizer
from keras.layers import Dense,Dropout
from keras.utils import np_utils
import numpy as np
from keras.layers import LSTM
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics

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

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=0)

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
cnn_lstm.add(Convolution1D(64, 3, border_mode="same",activation="relu",input_shape=(13, 1)))
cnn_lstm.add(MaxPooling1D(pool_length=2))
cnn_lstm.add(LSTM(lstm_output_size))
cnn_lstm.add(Dropout(0.1))
cnn_lstm.add(Dense(1, activation="sigmoid"))

# define optimizer and objective, compile cnn

cnn_lstm.compile(loss="mean_absolute_error", optimizer="adam", metrics=['mae'])

# train
cnn_lstm.fit(X_train, y_train, epochs=100, validation_data=(X_val, y_val))
cnn_lstm.save("cnn_lstm_model_right.hdf5")
