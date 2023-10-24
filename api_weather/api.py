import pandas as pd
from datetime import datetime
import holidays
from datetime import timedelta
class WeekendAnalyzer:
    def __init__(self, input_csv, output_csv):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.ru_holidays = holidays.Russia()

    def load_data(self):
        self.data = pd.read_csv(self.input_csv, sep=";")
        self.data["day"] = self.data["day"].astype(pd.Int64Dtype(), errors='ignore')
        self.data["month"] = self.data["month"].astype(pd.Int64Dtype(), errors='ignore')
        self.data["year"] = self.data["year"].astype(pd.Int64Dtype(), errors='ignore')

    def is_holiday(self, row):
        if pd.notna(row["year"]) and pd.notna(row["month"]) and pd.notna(row["day"]):
            date = datetime(year=int(row["year"]), month=int(row["month"]), day=int(row["day"]))
            if date in self.ru_holidays:
                return 1
            else:
                return 0

    def is_weekend(self, row):
        if pd.notna(row["year"]) and pd.notna(row["month"]) and pd.notna(row["day"]):
            date = datetime(year=int(row["year"]), month=int(row["month"]), day=int(row["day"]))
            return date.weekday()
        
    def prev_day(self):
        df = pd.read_csv(self.input_csv, delimiter=';')

        target = df['target'].tolist()
        count_of_str = len(target)
        prev_hour = [target[i-1] if i > 0 else target[0] for i in range(count_of_str)]
        prev_day = [target[i-24] if i > 23 else target[0] for i in range(count_of_str)]
        output_df = pd.DataFrame({'prev_day': prev_day, 'prev_hour': prev_hour})
        self.data = pd.concat([self.data, output_df], axis=1)
        
    def prev_day_hour_last(self, hours):
        df = pd.read_csv('files/weather_forecast.csv', delimiter=';')

        target = df['target'].tolist()[-1]
        prev_hour = [target] * hours
        prev_day = [target] * hours
        output_df = pd.DataFrame({'prev_day': prev_day, 'prev_hour': prev_hour})
        self.data = pd.concat([self.data, output_df], axis=1)
        
    def add_weekend_column(self):
        self.data["holiday"] = self.data.apply(self.is_holiday, axis=1)
        self.data['weekend'] = self.data.apply(self.is_weekend, axis=1)

    def save_output(self):
        self.data.to_csv(self.output_csv, sep=";", index=False)

    def analyze_test(self):
        self.load_data()
        self.add_weekend_column()
        self.prev_day()
        self.save_output()

    def analyze_pred(self, hours):
        self.load_data()
        self.add_weekend_column()
        self.prev_day_hour_last(hours)
        self.save_output()

