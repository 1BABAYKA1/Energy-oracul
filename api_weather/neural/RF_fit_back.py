import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor


df = pd.read_csv('files/weather_forecast.csv', delimiter=';')

y = df['target'].tolist()
df.pop('target')

x = df.values
count_of_columns = len(df.columns)

model = RandomForestRegressor(n_estimators=1000,
                            random_state=0,
                            criterion='squared_error',
                            max_features=0.33333,
                            oob_score=True,
                            max_depth=None)
model.fit(x, y)
with open('RF_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print('fit is done')

