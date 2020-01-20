import numpy as np
import time
from matplotlib import pyplot

start_time = time.time()

from keras.models import Sequential
from keras.layers import MaxPooling1D, Flatten, Conv1D
import pandas as pd
from sklearn.preprocessing import Normalizer
from keras.layers import Dense, Dropout

# To divide data into subsets, and in order to use cross-validation
from sklearn.model_selection import train_test_split, StratifiedKFold

data = pd.read_table('Capture Data/right_raspi_data_grosse.txt', delimiter=",", header=None)

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

scaler_train = Normalizer().fit(X_train)  # Inutile ?
X_train = scaler_train.transform(X_train)  # Normalisation des données
scaler_test = Normalizer().fit(X_test)
X_test = scaler_test.transform(X_test)

y_train = np.array(y_train)
y_test = np.array(y_test)
# reshape input to be [samples, time steps, features]
print(X_train.shape)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
# Permet juste de passer de dim = 2 à dim = 3, avec la troisième dim = 1.
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

kfold = StratifiedKFold(n_splits=10, shuffle=True)

cnn = Sequential()
cnn.add(
    Conv1D(64, 3, strides=1, activation="relu", input_shape=(12, 1), padding="valid", kernel_initializer='he_uniform',
           use_bias=True))
cnn.add(MaxPooling1D(pool_size=1))

cnn.add(Conv1D(128, 3, strides=1, activation="relu", padding="valid", kernel_initializer='he_uniform', use_bias=True))
cnn.add(MaxPooling1D(pool_size=1, strides=1))

cnn.add(Conv1D(256, 3, strides=1, activation="relu", padding="valid", kernel_initializer='he_uniform', use_bias=True))
cnn.add(MaxPooling1D(pool_size=2, strides=1))

cnn.add(Flatten())

cnn.add(Dense(128, activation="relu", kernel_initializer='he_uniform', use_bias=True))
cnn.add(Dropout(0.5))

cnn.add(Dense(1, activation="linear", kernel_initializer='he_uniform', use_bias=True))  # Used to do a regression
print(cnn.summary())

# Compile model
cnn.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])

maes = []

plot = True
for train, val in kfold.split(X_train, y_train):
    # Fit the model
    hist = cnn.fit(X_train[train], y_train[train], epochs=100, batch_size=32, verbose=0)
    # evaluate the model
    scores = cnn.evaluate(X_train[val], y_train[val], verbose=1)
    print("%s: %.2f" % (cnn.metrics_names[1], scores[1]))

    maes.append(scores[1])

    """Code to be used only to print nice plots """
    if plot:
        pyplot.plot(hist.history['mean_absolute_error'], "-r", label="Mean Absolute Error")
        pyplot.legend(loc="upper right")

        pyplot.xlabel("Epochs")
        pyplot.title("Evolution of the Mean Absolute Error during the training on one fold")
        pyplot.show()
        plot = False
        """"""

print("Averaged parameters : ")
print("Mean Absolute Error : ", "%.5f (+/- %.5f)" % (np.mean(maes), np.std(maes)))

cnn.save("cnn_model_right.hdf5")

interval = time.time() - start_time
print('Total time in seconds:', interval)
