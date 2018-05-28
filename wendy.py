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

aemet_url = 'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/07040'
headers = {
  'cache-control': "no-cache",
  'api_key': env['API-KEY'],
}

print(aemet_url)
print(headers)

r = requests.get(aemet_url, headers=headers)

response = json.loads(r.text)
