import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from sklearn.model_selection import KFold


ppg_dataset = np.loadtxt('part2_ppg.csv', delimiter=',')
bp_dataset = np.loadtxt('part2_bp.csv', delimiter=',')

print(len(bp_dataset))

# for data in ppg_dataset:
#     for i in range(len(data)):
#         if np.isinf(data[i]):
#             data[i] = -1000

cv = KFold(n_splits=10)

# for train_index, test_index in cv.split(X):
#     print("TRAIN:", train_index, "TEST:", test_index)
#     X_train, X_test = predictors[train_index], predictors[test_index]
#     y_train, y_test = targets[train_index], targets[test_index]
#
#     # For training, fit() is used
#     model.fit(X_train, y_train)
#
#     # Default metric is R2 for regression, which can be accessed by score()
#     model.score(X_test, y_test)
#
#     # For other metrics, we need the predictions of the model
#     y_pred = model.predict(X_test)
#
#     metrics.mean_squared_error(y_test, y_pred)
#     metrics.r2_score(y_test, y_pred)

X_train, X_test, y_train, y_test = train_test_split(ppg_dataset, bp_dataset, test_size=0.33, random_state=10)
X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5, random_state=10)

regressor = RandomForestRegressor(n_estimators=100,criterion="mse", verbose=2)
regressor.fit(X_train, y_train)

predictions = regressor.predict(X_test)
errors = abs(predictions - y_test)
print('Mean Absolute Error:', (np.mean(errors, axis=0)))
print(predictions[0:50])
print(y_test[0:50])

joblib.dump(regressor, "./random_forest_2.joblib")



