import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers.advanced_activations import LeakyReLU
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import load_model


X_train = np.loadtxt('parts1to6_ppg.csv', delimiter=',')
y_train = np.loadtxt('parts1to6_bp.csv', delimiter=',')

X_test = np.loadtxt('parts9_ppg.csv', delimiter=',')
y_test = np.loadtxt('parts9_bp.csv', delimiter=',')

X_val = np.loadtxt('parts8_ppg.csv', delimiter=',')
y_val = np.loadtxt('parts8_bp.csv', delimiter=',')

print(len(X_train))
print(len(X_test))
print(len(X_val))

model = Sequential()
model.add(Dense(128, input_dim = 21, activation='relu'))
model.add(Dense(128, activation='relu'))
# model.add(Dense(128, activation='relu'))
model.add(Dense(2, activation='relu'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=[tf.keras.metrics.MeanAbsoluteError()])
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=500, batch_size=128)

model.save("model_1to6_(128).h5")

# test
# model = load_model('model.h5')

predictions = model.predict(X_test)
print(predictions[0:20])
print(y_test[0:20])

errors = abs(y_test - predictions)
print('Mean Absolute Error:', np.mean(errors, axis=0))

errors = y_test - predictions
print('Standard Deviation: ', np.std(errors, axis=0))

