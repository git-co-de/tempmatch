import requests

base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
key = 'FHKBHS98MS8E8CBS4FF6CCBLP'

#mögliche Fehler als Klassen definieren: 
class MaximumRequestsDone(Exception):
    pass

class UndefinedLocation(Exception):
    pass

class WrongAPIKey(Exception):
    pass

class WrongDate(Exception):
    pass



def fetch_data_city(city, start, end):
    try: 
        url = f'{base_url}{city}/{start}/{end}'

        params = {"key": key,
                    "unitGroup": "metric",
                    "contentType": "json"}
        
        res = requests.get(url, params)
        
        return res.json()
    
    except ValueError as e:
        print(res.text)

        if "maximal number" in res.text:
            raise MaximumRequestsDone

        if "invalid location found" in res.text:
            raise UndefinedLocation

        if "API key" in res.text:
            raise WrongAPIKey

        if "cannot be before" in res.text:
            raise WrongDate



