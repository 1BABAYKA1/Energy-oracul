import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn.datasets
from sklearn.ensemble import RandomForestRegressor
import time
import pickle

# df = pd.read_csv('sample1.csv', delimiter=';')
# x = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
# y = df['Salary'].tolist()
# # x, y = sklearn.datasets.make_regression(n_samples=5000, n_features=10)
# regressor = RandomForestRegressor(n_estimators=100,
#                                   random_state=0)
#
# regressor.fit(x, y)
# Y_pred = regressor.predict(np.array([6.5]).reshape(1, 1))
# X_grid = np.arange(min(x)[0], max(x)[0], 0.01)
#
#
# # reshape for reshaping the data
# # into a len(X_grid)*1 array,
# # i.e. to make a column out of the X_grid value
# X_grid = X_grid.reshape((len(X_grid), 1))
#
# # Scatter plot for original data
# plt.scatter(x, y, color='blue')
#
# # plot predicted data
# plt.plot(X_grid, regressor.predict(X_grid),
#          color='green')
# plt.title('Random Forest Regression')
# plt.xlabel('Position level')
# plt.ylabel('Salary')
# plt.show()

index = -(24 * 30 + 480)

df = pd.read_csv('with_date_with_typeday_with_prev_day_with_prev_hour_one_weather2.csv', delimiter=';')
prev_pred = pd.read_csv('history_data.csv', delimiter=',')
y = df['target'][:index].tolist()
y_old = df['target'].tolist()
df.pop('target')
df.pop('year')
features = len(df.columns) - 1
x = df.iloc[:index, 1:].values
# for i in range(1, 11):
# regressor = RandomForestRegressor(n_estimators=1000, random_state=0, criterion='squared_error', max_features=0.33333,
#                                   oob_score=True, max_depth=None)
#
# regressor.fit(x, y)
# with open('rndf_without_year.pkl', 'wb') as f:
#     pickle.dump(regressor, f)

#
with open('rndf_without_year.pkl', 'rb') as f:
    regressor = pickle.load(f)

# x_grid = range(0, 480)


rp = []

for i in range(-index):
    next = regressor.predict(np.array(df.iloc[index + i, 1:]).reshape(1, features))
    rp.append(next[0])
    df.iloc[index + i + 1, 10] = next[0]
    df.iloc[index + i + 24, 9] = next[0]
    # if (i + 1) % 24 == 0:
    #     print(f'{df.iloc[index + i, 5]}.{df.iloc[-index + i, 6]}.{df.iloc[-index + i, 7]}', round(sum(rp[-24:]), 2))

# plt.scatter(x_grid, rp, color='green')
# plt.plot(x_grid, rp, color='green')
# plt.scatter(x_grid, y_old[-480:], color='red')
# plt.plot(x_grid, y_old[-480:], color='red')
pp = prev_pred['predict'].tolist()[index:]
# plt.scatter(x_grid, pp, color='blue')
# plt.plot(x_grid, pp, color='blue')
# plt.xlabel('Hours')
# plt.ylabel('Target')
p2p1 = []
p2p3 = []
p2p4 = []
for i in range(10 * 24):
    p1 = round(rp[i], 1)
    p2 = round(y_old[index + i], 1)
    p3 = round(pp[i])
    print(p1, p2, p3)
    p2p1.append(abs(round(p1 - p2, 1) / p2) * 100)
    p2p3.append(abs(round(p3 - p2, 1) / p2) * 100)
    p2p4.append(abs(round(round(y_old[index + i - 24], 1) - p2, 1) / p2) * 100)
    # p1 = round(sum(rp[i * 24: (i + 1) * 24]), 1)
    # p2 = round(sum(y_old[index + i * 24: index + (i + 1) * 24]), 1)
    # p3 = sum(pp[i * 24: (i + 1) * 24])
    # p2p1.append(abs(round(p1 - p2, 1)/p2) * 100)
    # p2p3.append(abs(round(p3 - p2, 1)/p2) * 100)
    # p2p4.append(abs(round(round(sum(y_old[index + (i - 1) * 24: index + i * 24]), 1) - p2, 1)/p2) * 100)
x_grid = range(1, 10 * 24 + 1)
print(regressor.oob_score_)
plt.grid(True, 'both')
plt.locator_params(axis='x', nbins=10)
plt.scatter(x_grid, p2p1, color='green')
plt.plot(x_grid, p2p1, color='green')
plt.scatter(x_grid, p2p3, color='blue')
plt.plot(x_grid, p2p3, color='blue')
plt.scatter(x_grid, p2p4, color='red')
plt.plot(x_grid, p2p4, color='red')
plt.show()

# for i in range(-10, 0):
#     y_pred = regressor.predict(np.array(df.iloc[i, 1:]).reshape(1, features))
#     print(y_pred)
