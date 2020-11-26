import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso

ppg_dataset = np.loadtxt('part2_ppg.csv', delimiter=',')
bp_dataset = np.loadtxt('part2_bp.csv', delimiter=',')

for data in ppg_dataset:
    for i in range(len(data)):
        if np.isinf(data[i]):
            data[i] = -1000

X_train, X_test, y_train, y_test = train_test_split(ppg_dataset, bp_dataset, test_size=0.33)
# X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5)


def linear_regression(X_train, y_train, X_test, y_test):
    regressor = LinearRegression(fit_intercept=True)
    regressor.fit(X_train, y_train)
    predictions = regressor.predict(X_test)
    print(y_test[0:20])
    print(predictions[0:20])

    errors = abs(y_test - predictions)
    print('Mean Absolute Error:', np.mean(errors, axis=0))


def lasso_regression(X_train, y_train, X_test, y_test, alpha):
    lasso = Lasso(alpha=alpha)
    lasso.fit(X_train, y_train)
    predictions = lasso.predict(X_test)
    print(y_test[0:20])
    print(predictions[0:20])

    errors = abs(y_test - predictions)
    print('Mean Absolute Error:', np.mean(errors, axis=0))

lasso_regression(X_train, y_train, X_test, y_test, 0.1)