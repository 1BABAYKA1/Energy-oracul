import numpy as np
import pandas as pd
import pickle


class Data:
    def __init__(self, time: int, day: int, month: int, year: int):
        self.time = time
        self.day = day
        self.month = month
        self.year = year

    def show_it(self):
        print(self.time, self.day, self.month, self.year)

    def convert_to_str(self):
        name = ''
        if self.time < 10:
            name += '0'
        name += str(int(self.time))
        name += ':00 '
        if self.day < 10:
            name += '0'
        name += str(self.day)
        name += '.'
        if self.month < 10:
            name += '0'
        name += str(self.month)
        name += '.'
        name += str(self.year)

        return name
    
def predict(filename, hours):
    test_df = pd.read_csv(f'files/result/{filename}', delimiter=';')
    hours_to_pred = int(hours)
    count_of_columns = len(test_df.columns)
    with open(f'neural/RF_model.pkl', 'rb') as f:
        model = pickle.load(f)

    list_of_dates = []
    our_prediction = []

    for i in range(hours_to_pred):
        cur_data = Data(test_df['time'][i],
                        test_df['day'][i],
                        test_df['month'][i],
                        test_df['year'][i])
        list_of_dates.append(cur_data.convert_to_str())

        next_hour = model.predict(np.array(test_df.iloc[i]).reshape(1, count_of_columns))
        our_prediction.append(round(next_hour[0], 1))
        if (i + 1) < len(test_df):
            test_df.iloc[(i + 1), -1] = next_hour[0]
        if (i + 24) < len(test_df):
            test_df.iloc[(i + 24), -2] = next_hour[0]

    output_df = pd.DataFrame({'Time': list_of_dates, 'Prediction': our_prediction})
    
    output_file_path = f'files/predict/{filename}.xlsx'
    output_df.to_excel(output_file_path, index=False)

    return output_file_path
