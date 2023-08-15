import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import warnings

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
        self.x = df.iloc[:-2, 1:]
        
    def train(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.regressor.fit(self.x, self.y)
        
    def predict(self, input_data):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            y_pred = self.regressor.predict(input_data)
        return y_pred[0]

if __name__ == "__main__":
    def make_predictions(predictor, hours):
        input_data = np.array(predictor.x.iloc[-2, :]).reshape(1, -1)
        input_data[0, 0] = hours
        prediction = predictor.predict(input_data)
        return prediction

    predictor = RandomForestPredictor('random_forest/data.csv')
    predictor.load_data()
    predictor.train()
    
    for hours in [1, 3, 6]:
        prediction = make_predictions(predictor, hours)
        print(f"Прогноз на {hours} часа(ов):", prediction)