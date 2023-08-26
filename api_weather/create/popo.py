import pandas as pd
from datetime import datetime, timedelta

def add_file(hours):
    current_hour = datetime.now().hour

    data = []
    for hour in range(current_hour, current_hour + hours):
        data.append({
            'time': hour % 24,
            'date': (datetime.now() + timedelta(hours=hour)).strftime('%d.%m.%Y')
        })
    df = pd.DataFrame(data)
    df = df[['time', 'date']]
    df.to_csv('files/input2.csv', index=False, sep=';')
    
add_file(hours=168)
