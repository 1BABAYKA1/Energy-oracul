import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Normalizer:
    def __init__(self, df):
        """
        Инициализация определяет как нужно нормализовать таблицу
        """
        self.col_about_power = 1
        self.col_about_other = df.shape[1] - self.col_about_power
        self.denominators = {}
        for col_name in df.iloc[:, 0:self.col_about_other]:
            self.denominators[col_name] = df[col_name].max()

        power_data = df.iloc[:, -self.col_about_power:]
        self.min_power, self.max_power = power_data.min().min(), power_data.max().max()

    def normalize(self, df):
        """
        Метод нормализации данных, можно использовать для подготовки данных к обучению модели, также потом
        используется для нормализации данных при работе готовой модели
        """
        for col_name in df.iloc[:, 0:self.col_about_other]:
            df[col_name] /= self.denominators[col_name]

        for col_name in df.iloc[:, -self.col_about_power:]:
            df[col_name] = (df[col_name] - self.min_power) / (self.max_power - self.min_power)
        return df

    def denormalize_answer(self, predict):
        """
        Модель предсказывает число от 0 до 1, эта функция принимает предсказание(предсказания)
        и возвращает количество потребляемой энергии в мегаваттах.

        Attributes
        ----------------
        predict: Pandas Series / Numpy array / float
            Значение, предсказанное моделью

        ----------------
        Значение возвращается тем же типом данных, что и predict
        """
        return predict * (self.max_power - self.min_power) + self.min_power


df = pd.read_csv('with_date_with_typeday_with_prev_day_with_prev_hour_one_weather.csv', delimiter=';')
normalizer = Normalizer(df)
df = normalizer.normalize(df)
TEST_SIZE = 0.05
TEST_INDEX = -int(len(df) * TEST_SIZE)
y_train = df['target'][:TEST_INDEX].values
y_test = df['target'][TEST_INDEX:].values
df.pop('target')
df.pop('Unnamed: 0')
df.pop('year')
num_features = len(df.iloc[0])
x_train = df.iloc[:TEST_INDEX].values
x_test = df.iloc[TEST_INDEX:].values
# print(x_train)
# print(x_test)
# Note that when using the delayed-build pattern (no input shape specified),
# the model gets built the first time you call `fit`, `eval`, or `predict`,
# or the first time you call the model on some input data.
model = tf.keras.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dense(1))
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.05, nesterov=False), loss='mse')
# This builds the model for the first time:
model.fit(x_train, y_train, batch_size=32, epochs=30)
y_pred = []
for i in range(len(x_test)):
    y_pred.append(np.array(model(x_test[i].reshape(1, num_features)))[0][0])
    if (i + 1) < len(x_test):
        x_test[i + 1, 7] = y_pred[-1]
    if (i + 24) < len(x_test):
        x_test[i + 24, 6] = y_pred[-1]
# y_pred = np.array(model.predict(x_test, batch_size=-TEST_INDEX)).reshape(-1)
y_pred = np.array(y_pred)
y_pred = normalizer.denormalize_answer(y_pred)
y_test = normalizer.denormalize_answer(y_test)
print('evl', model.evaluate(x_test, y_test), 'evl')
print('sum_er', np.sum(np.array(tf.keras.metrics.mean_absolute_error(y_test, y_pred))), 'sum_er')
x_grid = range(1, 1 - TEST_INDEX)
plt.scatter(x_grid, y_pred, color='green')
plt.plot(x_grid, y_pred, color='green')
plt.scatter(x_grid, y_test, color='red')
plt.plot(x_grid, y_test, color='red')
plt.show()
