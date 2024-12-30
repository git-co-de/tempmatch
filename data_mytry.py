import pandas as pd

#tägliche Wetterdaten bekommen
def get_daily(data):
    if not isinstance(data, dict):
        print('Hier ist etwas schief gelaufen')
        return None

    indices = []
    temp = []


    for d in data["days"]: 
        indices.append(d["datetime"])
        temp.append(d["temp"])

    
    df = pd.DataFrame(data = {f"{data['address']}": temp}, index = indices)

    return df


def get_hourly(data):
    if not isinstance(data, dict):
        print('Hier ist etwas schief gelaufen')
        return None

    indices = []
    temp = []


    for day in data["days"]: 
        for hour in day["hours"]:
            indices.append(f'{day["datetime"]} {hour["datetime"]}')
            temp.append(hour["temp"])
    
    
    df = pd.DataFrame(data = {f"{data['address']}": temp}, index = indices)

    return df