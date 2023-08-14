# Importing pandas to open the csv file
import pandas as pd


def read_data():
    data = pd.read_csv('data.csv')
    data = data.dropna()
    data = data.reset_index(drop=True)
    data = data.drop(['predict', 'temp_pred', 'weather_pred'], axis=1)
    data = data.astype('float32')
    return data