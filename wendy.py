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
sun_up = current_prediction['orto']
sun_down = current_prediction['ocaso']
date = current_prediction['fecha']

filtered_data = {i:{} for i in range(0, 24)}

for data_type in ('precipitacion', 'temperatura', 'sensTermica', 'estadoCielo'):
  for i in current_prediction[data_type]:
    value_name = 'value' if not data_type == 'estadoCielo' else 'descripcion'
    filtered_data[int(i['periodo'])][data_type]  = i[value_name]

msg = """
Morning!

Today, {date} sun rises at {sun_up} and sets at {sun_down}, on {city}, {state}.

Detailed information:
""".format(date=date, sun_up=sun_up, sun_down=sun_down, city=city, state=state)

hour_line = "\t{time}h : {temp}º ({sens_termica}), {prob_lluvia}% lluvia y con el cielo {estado_cielo}\n"

for i in filtered_data:
  if len(filtered_data[i].keys()) == 0:
    continue
  msg = msg + hour_line.format(
      time=i,
      temp=filtered_data[i]['temperatura'],
      sens_termica=filtered_data[i]['sensTermica'],
      prob_lluvia=filtered_data[i]['precipitacion'],
      estado_cielo=filtered_data[i]['estadoCielo']
    )

print(msg)