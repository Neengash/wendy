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
orto = current_prediction['orto']
ocaso = current_prediction['ocaso']
dia = current_prediction['fecha']
print("Dia {} el sol sale a las {} y se pone a las {} en {}, {}".format(dia, orto, ocaso, city, state))

precipitacion = current_prediction['precipitacion']
temp = current_prediction['temperatura']
sens_termica = current_prediction['sensTermica']
sky = current_prediction['estadoCielo']

filtered_data = {i:{} for i in range(0, 24)}

for data_type in ('precipitacion', 'temperatura', 'sensTermica', 'estadoCielo'):
  for i in current_prediction[data_type]:
    value_name = 'value' if not data_type == 'estadoCielo' else 'descripcion'
    filtered_data[int(i['periodo'])][data_type]  = i[value_name]

print(filtered_data)
