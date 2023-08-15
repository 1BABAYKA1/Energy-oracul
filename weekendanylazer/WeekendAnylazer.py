import pandas as pd
from datetime import datetime
import holidays

class WeekendAnalyzer:
    def __init__(self, input_csv, output_csv):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.ru_holidays = holidays.Russia()

    def load_data(self):
        self.data = pd.read_csv(self.input_csv, sep=";")
        self.data["day"] = self.data["day"].astype(int)
        self.data["month"] = self.data["month"].astype(int)
        self.data["year"] = self.data["year"].astype(int)

    def is_weekend_or_holiday(self, row):
        date = datetime(year=int(row["year"]), month=int(row["month"]), day=int(row["day"]))
        if date.weekday() >= 5:
            return 1
        elif date in self.ru_holidays:
            return 1
        else:
            return 0

    def add_weekend_column(self):
        self.data["weekend"] = self.data.apply(self.is_weekend_or_holiday, axis=1)
        self.data = self.data.drop(columns=['id'])

    def save_output(self):
        self.data.to_csv(self.output_csv, sep=";", index=False)

    def analyze(self):
        self.load_data()
        self.add_weekend_column()
        self.save_output()

if __name__ == "__main__":
    analyzer = WeekendAnalyzer("random_forest/data.csv", "data.csv")
    analyzer.analyze()
