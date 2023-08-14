import pandas as pd

class CSVColumnRemover:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def remove_columns(self, columns_to_remove):
        data = pd.read_csv(self.input_file)
        data = data.drop(columns=columns_to_remove)
        data.to_csv(self.output_file, index=False)

input_file = 'data_edit/data.csv'
output_file = 'data_now.csv'
columns_to_remove = ['predict', 'temp_pred', 'weather_pred']

csv_remover = CSVColumnRemover(input_file, output_file)
csv_remover.remove_columns(columns_to_remove)
