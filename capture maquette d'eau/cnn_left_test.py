from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.models import Sequential
from keras.layers import Convolution1D,MaxPooling1D, Flatten
import pandas as pd
from sklearn.preprocessing import Normalizer
import numpy as np
from keras.layers import Dense, Dropout
from sklearn.metrics import precision_score, accuracy_score, recall_score, f1_score, confusion_matrix


#traindata = pd.read_csv('kdd/kddtrain.csv', header=None)
testdata = pd.read_table('left_raspi_data.txt', header=None, delimiter=",")

	#Hex to int the testing data !
liste_2 = []
liste_3 = []
for value in testdata.iloc[:,0]:
	liste_2.append(int(value, base=16))
testdata.iloc[:,0]=liste_2
for value in testdata.iloc[:,2]:
	liste_3.append(int(value, base=16))
testdata.iloc[:,2]=liste_3

C = testdata.iloc[:,13]
T = testdata.iloc[:,0:13]

scaler = Normalizer().fit(T)
testT = scaler.transform(T)


y_test = np.array(C)


X_test = np.reshape(testT, (testT.shape[0],testT.shape[1],1))


lstm_output_size = 128

cnn = Sequential()
cnn.add(Convolution1D(64, 3, border_mode="same",activation="relu",input_shape=(13, 1)))
cnn.add(MaxPooling1D(pool_length=(2)))
cnn.add(Flatten())
cnn.add(Dense(128, activation="relu"))
cnn.add(Dropout(0.5))
cnn.add(Dense(1, activation="sigmoid"))


cnn.load_weights("cnn_model_left.hdf5")


y_pred = cnn.predict_classes(X_test)
#np.savetxt("cnn.txt", y_pred)
accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred , average="micro")
precision = precision_score(y_test, y_pred , average="micro")
f1 = f1_score(y_test, y_pred, average="micro")

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



