import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

def learn(filename):
    df = pd.read_csv(f'files/learn/l_{filename}', delimiter=';')

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
    with open(f'neural/{filename}.pkl', 'wb') as f:
        pickle.dump(model, f)
