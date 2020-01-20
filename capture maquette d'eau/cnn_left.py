from __future__ import print_function
import numpy as np
#np.random.seed(1337)  # for reproducibility

from keras.models import Sequential
from keras.layers import Convolution1D,MaxPooling1D, Flatten
import pandas as pd
from sklearn.preprocessing import Normalizer
from keras.layers import Dense, Dropout
import numpy as np


traindata = pd.read_table('./Capture Data/left_raspi_data4.txt', delimiter=",", header=None)
testdata = pd.read_table('./Capture Data/left_raspi_data1.txt', header=None, delimiter=",")

#Conversion from hexa to int when needed...

def to_decimal(data) :
	liste_0 = []
	liste_1 = []
	for value in data.iloc[:,0]:
		liste_0.append(int(value, base=16))
	data.iloc[:,0]=liste_0
	for value in data.iloc[:,2]:
		liste_1.append(int(value, base=16))
	data.iloc[:,2]=liste_1
	return data
	
	#In the training data
traindata = to_decimal(traindata)

	#In the testing data !
testdata = to_decimal(testdata)

#=======

X = traindata.iloc[:,0:15]
Y = traindata.iloc[:,15]
C = testdata.iloc[:,15]
T = testdata.iloc[:,0:15]

scaler = Normalizer().fit(X) #Inutile ? 
trainX = scaler.transform(X) #Normalisation des données

scaler = Normalizer().fit(T)
testT = scaler.transform(T)

y_train = np.array(Y)
y_test = np.array(C)


# reshape input to be [samples, time steps, features]
X_train = np.reshape(trainX, (trainX.shape[0],trainX.shape[1],1))
X_test = np.reshape(testT, (testT.shape[0],testT.shape[1],1))


#Model definition
cnn = Sequential()
	#Stacking of layers one after the other
cnn.add(Convolution1D(64, 3, padding="same",activation="relu",input_shape=(15, 1))) #64 filtres et 3 en longueur de weight matrix, donc en gros on fait 64 convolutions sur le même vecteur.
#input_shape = batch dimension not included => No need to know how many samples are in the data set (/ the batch) I guess
#
# On a donc une matrice de 13*1*64 en termes de dimensions en sortie de la première couche.
cnn.add(MaxPooling1D(pool_size=2)) # For temporal data only ? # On divise par deux en termes de dimensions donc on a (7,1)
cnn.add(Flatten())
cnn.add(Dense(128, activation="relu")) #2D layer
cnn.add(Dropout(0.5))
cnn.add(Dense(1, activation="sigmoid"))
print(cnn.summary())


# define optimizer and objective, compile cnn
cnn.compile(loss="binary_crossentropy", optimizer="adam",metrics=['accuracy'])

# train
cnn.fit(X_train, y_train, epochs=2, verbose=1,validation_data=(X_test, y_test))
cnn.save("cnn_model_left.hdf5")

