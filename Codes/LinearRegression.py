import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
import joblib

X_train = np.loadtxt('parts6_ppg.csv', delimiter=',')
y_train = np.loadtxt('parts6_bp.csv', delimiter=',')

X_test = np.loadtxt('parts9_ppg.csv', delimiter=',')
y_test = np.loadtxt('parts9_bp.csv', delimiter=',')

def linear_regression(X_train, y_train, X_test, y_test):
    regressor = LinearRegression(fit_intercept=True)
    regressor.fit(X_train, y_train)
    predictions = regressor.predict(X_test)
    print(y_test[1000:1020])
    print(predictions[1000:1020])

    errors = abs(y_test - predictions)
    print('Mean Absolute Error:', np.mean(errors, axis=0))
    print('Standard Deviation:', np.std(errors, axis=0))
    joblib.dump(regressor, "./linear_6.joblib")


def lasso_regression(X_train, y_train, X_test, y_test, alpha):
    lasso = Lasso(alpha=alpha)
    lasso.fit(X_train, y_train)
    predictions = lasso.predict(X_test)
    print(y_test[150:170])
    print(predictions[150:170])

    errors = abs(y_test - predictions)
    print('Mean Absolute Error:', np.mean(errors, axis=0))
    print('Standard Deviation:', np.std(errors, axis=0))
    joblib.dump(lasso, "./lasso_1to6.joblib")


# lasso_regression(X_train, y_train, X_test, y_test, 0.1)
linear_regression(X_train, y_train, X_test, y_test)