import pandas as pd

# Загрузка данных из CSV
input_file = 'files/input_ex.csv'  # Замените на имя вашего файла
data = pd.read_csv(input_file, delimiter=';')

# Создание нового столбца "date" путем объединения "day", "month" и "year"
data['date'] = data['day'].astype(str) + '.' + data['month'].astype(str) + '.' + data['year'].astype(str)

# Удаление столбцов "day", "month" и "year"
data = data.drop(['day', 'month', 'year'], axis=1)

# Сохранение данных с новым столбцом "date"
output_file = 'files/data_with_date_column.csv'
data.to_csv(output_file, index=False, sep=';')

print(f"Данные сохранены с новым столбцом 'date' в файле {output_file}")
