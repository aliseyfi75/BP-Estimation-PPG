import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers.advanced_activations import LeakyReLU
from sklearn.model_selection import train_test_split
import tensorflow as tf



ppg_dataset = np.loadtxt('part2_ppg.csv', delimiter=',')
bp_dataset = np.loadtxt('part2_bp.csv', delimiter=',')

for data in ppg_dataset:
    for i in range(len(data)):
        if np.isinf(data[i]):
            data[i] = -1000

# sc = MinMaxScaler()
# ppg_dataset = sc.fit_transform(ppg_dataset)
# bp_dataset.reshape(-1, 1)
# bp_dataset = sc.fit_transform(bp_dataset)

X_train, X_test, y_train, y_test = train_test_split(ppg_dataset, bp_dataset, test_size=0.33)
X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5)

model = Sequential()
model.add(Dense(60, input_dim = 21, activation='relu'))
model.add(Dense(60, activation='relu'))
model.add(Dense(60, activation='relu'))
model.add(Dense(2, activation='relu'))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=[tf.keras.metrics.MeanAbsoluteError()])
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=500, batch_size=128)

# model.save("model.h5")

predictions = model.predict(X_test)
print(predictions[0:20])
print(y_test[0:20])

errors = abs(y_test - predictions)
print('Mean Absolute Error:', np.mean(errors, axis=0))

