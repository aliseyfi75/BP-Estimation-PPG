from sklearn.model_selection import GridSearchCV
from sklearn import neighbors
import numpy as np
from sklearn.model_selection import train_test_split


ppg_dataset = np.loadtxt('part2_ppg.csv', delimiter=',')
bp_dataset = np.loadtxt('part2_bp.csv', delimiter=',')

for data in ppg_dataset:
    for i in range(len(data)):
        if np.isinf(data[i]):
            data[i] = -1000

X_train, X_test, y_train, y_test = train_test_split(ppg_dataset, bp_dataset, test_size=0.33)

params = {'n_neighbors':[2,3,4,5,6,7,8,9]}

knn = neighbors.KNeighborsRegressor()

model = GridSearchCV(knn, params, cv=5)
model.fit(X_train,y_train)
model.best_params_

predictions = model.predict(X_test)
print(predictions[0:20])
print(y_test[0:20])

errors = abs(predictions - y_test)
print('Mean Absolute Error:', (np.mean(errors, axis=0)))