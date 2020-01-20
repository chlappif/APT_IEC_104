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