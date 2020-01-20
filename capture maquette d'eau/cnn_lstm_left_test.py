from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Convolution1D,MaxPooling1D
import pandas as pd

from sklearn.preprocessing import Normalizer
import numpy as np
from keras.layers import LSTM
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score, confusion_matrix


traindata = pd.read_table('left_raspi_data.txt', delimiter=",", header=None)
testdata = pd.read_table('left_raspi_test_data.txt', header=None, delimiter=",")


##Conversion from hexa to int when needed...
	#In the training data
liste_0 = []
liste_1 = []
for value in traindata.iloc[:,0]:
	liste_0.append(int(value, base=16))
traindata.iloc[:,0]=liste_0
for value in traindata.iloc[:,2]:
	liste_1.append(int(value, base=16))
traindata.iloc[:,2]=liste_1

	#In the testing data !
liste_2 = []
liste_3 = []
for value in testdata.iloc[:,0]:
	liste_2.append(int(value, base=16))
testdata.iloc[:,0]=liste_2
for value in testdata.iloc[:,2]:
	liste_3.append(int(value, base=16))
testdata.iloc[:,2]=liste_3
#==========================================

X = traindata.iloc[:,0:13]
Y = traindata.iloc[:,13]
C = testdata.iloc[:,13]
T = testdata.iloc[:,0:13]

scaler = Normalizer().fit(X)
trainX = scaler.transform(X)

scaler = Normalizer().fit(T)
testT = scaler.transform(T)

y_train = np.array(Y)
y_test = np.array(C)


# reshape input to be [samples, time steps, features]
X_train = np.reshape(trainX, (trainX.shape[0],trainX.shape[1],1))
X_test = np.reshape(testT, (testT.shape[0],testT.shape[1],1))

lstm_output_size = 70

cnn = Sequential()
cnn.add(Convolution1D(64, 3, border_mode="same",activation="relu",input_shape=(13, 1)))
cnn.add(MaxPooling1D(pool_length=(2)))
cnn.add(LSTM(lstm_output_size))
cnn.add(Dropout(0.1))
cnn.add(Dense(1, activation="sigmoid"))

# load model

cnn.load_weights("cnn_lstm_model_left.hdf5")


cnn.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
loss, accuracy = cnn.evaluate(X_test, y_test)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))


y_pred = cnn.predict_classes(X_test)
accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred , average="micro")
precision = precision_score(y_test, y_pred , average="micro")
f1 = f1_score(y_test, y_pred, average="micro")
#np.savetxt('res/expected1.txt', y_test, fmt='%01d')
#np.savetxt('res/predicted1.txt', y_pred, fmt='%01d')

print("confusion matrix")
print("----------------------------------------------")
print("accuracy")
print("%.6f" %accuracy)
print("racall")
print("%.6f" %recall)
print("precision")
print("%.6f" %precision)
print("f1score")
print("%.6f" %f1)
print("confusion matrix")
cm = confusion_matrix(y_test, y_pred)
print(cm)
print("==============================================")

