import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import warnings
from datetime import datetime

class RandomForestPredictor:
    def __init__(self, data_path, n_estimators=100, random_state=0):
        self.data_path = data_path
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.regressor = RandomForestRegressor(n_estimators=self.n_estimators, random_state=self.random_state)
        
    def load_data(self):
        df = pd.read_csv(self.data_path, delimiter=';')
        self.y = df['target'][:-2].tolist()
        df.pop('target')
        self.x = df.iloc[:-2, 2:]  # Учитываем только столбцы с температурой и далее
        
    def train(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.regressor.fit(self.x, self.y)
        
    def predict(self, input_data):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            y_pred = self.regressor.predict(input_data)
        return y_pred[0]  # Распаковываем значение из массива

if __name__ == "__main__":
    def make_predictions(predictor, hours, day, month, year):
        input_data = np.array(predictor.x.iloc[-2, :]).reshape(1, -1)
        input_data[0, 0] = hours
        input_data[0, 1] = int(day)  # Преобразуем в целое число
        input_data[0, 2] = int(month)  # Преобразуем в целое число
        input_data[0, 3] = int(year)  # Преобразуем в целое число
        prediction = predictor.predict(input_data)
        return prediction

    # Создание функции для определения выходного дня
    def is_weekend(day, month, year):
        dt = datetime(year, month, day)
        return dt.weekday() >= 5  # В России суббота и воскресенье

    predictor = RandomForestPredictor('random_forest/data.csv')
    predictor.load_data()
    predictor.train()
    
    df = pd.read_csv('random_forest/data.csv', delimiter=';')
    df['Weekend'] = df.apply(lambda row: 1 if is_weekend(row['day'], row['month'], row['year']) else 0, axis=1)
    
    for index, row in df.iterrows():
        prediction = make_predictions(predictor, row['time'], row['day'], row['month'], row['year'])
        print(f"День {row['day']}.{row['month']}.{row['year']} Вых.:{row['Weekend']} Прогноз: {prediction}")
    
    # Отрисовка графиков
    prev_pred = pd.read_csv('forestbyvovaputin/history_data.csv', delimiter=',')
    y_old = df['target'].tolist()
    x_grid = range(0, 24)
    
    plt.scatter(x_grid, regressor.predict(np.array(df.iloc[-480:-456, 1:])), color='green', label='Predicted (New Model)')
    plt.plot(x_grid, regressor.predict(np.array(df.iloc[-480:-456, 1:])), color='green')
    
    plt.scatter(x_grid, y_old[-480:-456], color='red', label='Actual')
    plt.plot(x_grid, y_old[-480:-456], color='red')
    
    plt.scatter(x_grid, prev_pred['predict'].tolist()[-480:-456], color='blue', label='Predicted (Previous Model)')
    plt.plot(x_grid, prev_pred['predict'].tolist()[-480:-456], color='blue')
    
    plt.xlabel('Hours')
    plt.ylabel('Target')
    plt.legend()
    plt.show()
