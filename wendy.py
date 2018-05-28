env = {}

def load_env_values():
  with open('.env', 'r') as f:
    for line in f:
      key_value = line.split('=')
      env[key_value[0]] = key_value[1]
  return env

print("Hi I'm Wendy")

env = load_env_values()

