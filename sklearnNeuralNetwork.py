import numpy
import pandas
from sklearn.neural_network import MLPRegressor
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error, max_error
import matplotlib.pyplot as plt

df = pd.read_csv('with_date_with_typeday_with_prev_day_with_prev_hour_one_weather.csv', delimiter=';')
target = df['target'].tolist()
df.pop('target')
df.pop('Unnamed: 0')
df.pop('year')
for i in range(len(df)):
    day_month = (df.iloc[i, 5] - 1) * 31 + df.iloc[i, 4]
df.pop('day')
df.pop('month')
df['daymonth'] = day_month
df['target'] = target


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


normalizer = Normalizer(df)
df = normalizer.normalize(df)
TEST_SIZE = 0.05

# Разбиение дасасета на train и test.
train_num = int(len(df) * (1 - TEST_SIZE))
x_train, y_train = df.iloc[:train_num, :-1], df.iloc[:train_num, -1]
x_test, y_test = df.iloc[train_num:, :-1], df.iloc[train_num:, -1]
# Ну тут понятно все
# (96, 78, 53, 17, 31)
# (60, 50)
reg = MLPRegressor(hidden_layer_sizes=(60, 40), activation='relu',
                   solver="adam", alpha=0.0007, batch_size="auto", shuffle=True,
                   learning_rate='adaptive', learning_rate_init=0.01,
                   power_t=0.5, max_iter=200, verbose=True, tol=0.0001)

reg.fit(x_train.values, y_train)
print("Train accuracy: {}".format(reg.score(x_train, y_train)))
print("Test accuracy:  {}".format(reg.score(x_test, y_test)))

y_pred = []
for i in range(len(x_test)):
    pred = reg.predict(x_test.iloc[i].to_numpy().reshape(1, len(x_test.iloc[i])))
    y_pred.append(pred[0])
    try:
        x_test.iloc[i + 1, 'prev_hour'] = pred[0]
    except Exception:
        pass
    try:
        x_test.iloc[i + 24, 'prev_day'] = pred[0]
    except Exception:
        pass
y_pred = normalizer.denormalize_answer(numpy.array(y_pred))
y_test = y_test.to_numpy()
y_test = normalizer.denormalize_answer(y_test)

print(mean_absolute_percentage_error(y_pred, y_test))
print(max_error(y_pred, y_test))
# for i in range(-24, 0):
#     print(y_test[i], round(y_pred[i], 3))

plt.plot(y_test.reshape(-1), color='red')
plt.plot(y_pred.reshape(-1), color='green')
plt.show()
