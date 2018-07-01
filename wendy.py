import requests
import json
import smtplib
import datetime
from email.mime.text import MIMEText

env = {}

def load_env_values():
  with open('.env', 'r') as f:
    for line in f:
      line = line.split('\n')[0]
      key_value = line.split('=')
      env[key_value[0]] = key_value[1]
  return env

def format_rain(value):
    if value == "Ip" or value == 0:
        return ", {value}% lluvia".format(value=value)
    else:
        return ""

env = load_env_values()

aemet_url = 'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/{location}'
location_url = aemet_url.format(location=env['LOCATION'])
headers = {
  'cache-control': "no-cache",
  'api_key': env['API-KEY'],
}

r = requests.get(location_url, headers=headers).json()
r2 = requests.get(r['datos']).json()[0]

city = r2['nombre']
state = r2['provincia']

now = datetime.datetime.now()

current_prediction = r2['prediccion']['dia'][0]
if (datetime.datetime.strptime(current_prediction['fecha'], "%Y-%m-%d").day != now.day):
  current_prediction = r2['prediccion']['dia'][1]

date = current_prediction['fecha']
sun_up = current_prediction['orto']
sun_down = current_prediction['ocaso']
date = current_prediction['fecha']

filtered_data = {i:{} for i in range(0, 24)}

for data_type in ('precipitacion', 'temperatura', 'sensTermica', 'estadoCielo'):
  for i in current_prediction[data_type]:
    value_name = 'value' if not data_type == 'estadoCielo' else 'descripcion'
    filtered_data[int(i['periodo'])][data_type]  = i[value_name]


body = """
Morning!

Today, {date} sun rises at {sun_up} and sets at {sun_down}, on {city}, {state}.

That's the info I could get:

""".format(date=date, sun_up=sun_up, sun_down=sun_down, city=city, state=state)

hour_line = "\t{time}h : {temp}º ({sens_termica}) {lluvia} y con el cielo {estado_cielo}\n"

for i in filtered_data:
  if len(filtered_data[i].keys()) == 0:
    continue
  body = body + hour_line.format(
      time=i,
      temp=filtered_data[i]['temperatura'],
      sens_termica=filtered_data[i]['sensTermica'],
      lluvia=format_rain(filtered_data[i]['precipitacion']),
      estado_cielo=filtered_data[i]['estadoCielo']
    )

msg = MIMEText(body)
msg['Subject'] = 'Wake up {name}'.format(name=env['NAME'])
msg['From'] = env['FROM']
msg['To'] = env['TO']

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
