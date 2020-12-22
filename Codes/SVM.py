from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor

X_train = np.loadtxt('parts8_ppg_5.csv', delimiter=',')
y_train = np.loadtxt('parts1to6_bp_5.csv', delimiter=',')

X_test = np.loadtxt('parts9_ppg_5.csv', delimiter=',')
y_test = np.loadtxt('parts9_bp_5.csv', delimiter=',')

#
#
# X_train, X_test, y_train, y_test = train_test_split(ppg_dataset, bp_dataset, test_size=0.33)
# X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5)

sc_X = StandardScaler()
sc_Y = StandardScaler()
X = sc_X.fit_transform(X_train)
Y = sc_Y.fit_transform(y_train)

regressor = MultiOutputRegressor(SVR(kernel= 'rbf', verbose= 1))
regressor.fit(X, Y)

predictions = regressor.predict(X_test)
print(y_test[0:20])
print(predictions[0:20])

errors = abs(y_test - predictions)
print('Mean Absolute Error:', np.mean(errors, axis=0))
print('Standard Deviation:', np.std(errors, axis=0))
