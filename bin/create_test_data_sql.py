import random

from datetime import datetime

if __name__ == '__main__':
    now = datetime.now()
    query = (
        'DELETE FROM devroom_status;\n'
        'INSERT \n'
        'INTO devroom_status (temperature, humidity, co2, created_at) \n'
        'VALUES \n'
    )
    temperature = 25.0
    humidity = 60.0
    co2 = 500
    for i in range(60):
        date = now.replace(
            minute=i
        )
        query += (
            f"({temperature}, {humidity}, {co2}, '{date}'),\n"
        )
        temperature = round(random.uniform(temperature - 1 if temperature > -5 else temperature, temperature + 1 if temperature < 40 else temperature), 1)
        humidity = round(random.uniform(humidity - 5 if humidity > 5.1 else humidity, humidity + 5 if humidity < 94.9 else humidity), 1)
        co2 = random.randint(co2 - 100 if co2 > 101 else co2, co2 + 100 if co2 < 5000 else co2)
        
    else:
        query = query.rstrip(',\n') + ';'
    
    with open('bin/sql/test_data.sql', mode='w', encoding='utf-8') as f:
        f.write(query)