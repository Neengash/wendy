import requests
import json

env = {}

def load_env_values():
  with open('.env', 'r') as f:
    for line in f:
      line = line.split('\n')[0]
      key_value = line.split('=')
      env[key_value[0]] = key_value[1]
  return env

env = load_env_values()

aemet_url = 'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/{}'.format(env['LOCATION'])
headers = {
  'cache-control': "no-cache",
  'api_key': env['API-KEY'],
}

r = requests.get(aemet_url, headers=headers).json()
r2 = requests.get(r['datos']).json()[0]

city = r2['nombre']
state = r2['provincia']
current_prediction = r2['prediccion']['dia'][0]

print("El tiempo de {} - {}".format(city, state))
print(r2['prediccion']['dia'][0].keys())
