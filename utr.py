import requests
import json

def _getmonitors_(apikey):
  url = 'https://api.uptimerobot.com/v2/getMonitors'
 
  payload = 'api_key=' + apikey + '&format=json&logs=0'
  headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'cache-control': 'no-cache'
  }
 
  response = requests.request('POST', url, data=payload, headers=headers)
  if response.status_code is not 200:
    raise "HTTP ERROR " + response.status_code

  data = json.loads(response.text)
  stat = data['stat']
  if stat == 'fail':
    if data['error']['type'] == 'invalid_parameter' and data['error']['parameter_name'] == 'api_key':
      raise Exception('Invalid API key')
    else:
      raise Exception(data['error']['type'])

  return data['monitors']

def getmonitorcounts(apikey, ignore_paused):
  error = None
  up = 0
  down = 0
  paused = 0
  unknown = 0
  total = 0

  try:
    monitors = _getmonitors_(apikey)
  
    for monitor in monitors:
      status = monitor['status']
      if status == 0:
        if not ignore_paused:
          paused = paused + 1
          total = total + 1
      else:
        total = total + 1
        if status == 2:
          up = up + 1
        elif status == 8 or status == 9:
          down = down + 1
        else:
          unknown = unknown + 1

  except Exception as e:
    error = e

  return [error, up, down, paused, unknown, total]


