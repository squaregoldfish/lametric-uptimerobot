#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,cgi,cgitb
import traceback
import json
import requests
cgitb.enable()

def _getmonitors_(apikey):
  url = 'https://api.uptimerobot.com/v2/getMonitors'

  payload = 'api_key=' + apikey + '&format=json&logs=0'
  headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'cache-control': 'no-cache'
  }

  response = requests.request('POST', url, data=payload, headers=headers)
  if response.status_code != 200:
    raise Exception("HTTP ERROR " + str(response.status_code))

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
    print(traceback.format_exc())
    error = e

  return [error, up, down, paused, unknown, total]

error = None
up = 0
down = 0
paused = 0
unknown = 0
total = 0

try:
  arguments = cgi.FieldStorage()
  apikey = arguments.getvalue('apikey')
  ignore_paused = (arguments.getvalue('ignorePaused') == 'true')

  if apikey is None:
    error = 'Missing apikey'
  else:
    monitor_info = getmonitorcounts(apikey, ignore_paused)

    error = monitor_info[0]
    up = monitor_info[1]
    down = monitor_info[2]
    paused = monitor_info[3]
    unknown = monitor_info[4]
    total = monitor_info[5]
    if up == total:
      up = 'All'

except Exception as e:
  error = e

sys.stdout.write('Content-type: application/json\n\n')

if error is not None:
  with open('/home/squaregoldfish/temp/lametric-uptimerobot-monitors.err', 'a') as f:
    f.write(arguments)
    f.write('\n')
    f.write(repr(error))
    f.write('\n')

  sys.stdout.write('{"frames":[{"text":"Cannot retrieve Uptime Robot status","icon":"i23080"}]}')
else:
  output = {}
  output['frames'] = []

  upout = {}
  upout['text'] = str(up) + ' ↑'
  upout['icon'] = 'i41593'
  output['frames'].append(upout)

  if down > 0:
    downout = {}
    downout['text'] = str(down) + ' ↓'
    downout['icon'] = 'i41594'
    output['frames'].append(downout)

  if paused > 0:
    pausedout = {}
    pausedout['text'] = str(paused) + ' II'
    pausedout['icon'] = 'i41595'
    output['frames'].append(pausedout)
   

  if unknown > 0:
    unknownout = {}
    unknownout['text'] = str(unknown) + ' ???'
    unknownout['icon'] = 'i41595'
    output['frames'].append(unknownout)

  sys.stdout.write(json.dumps(output))

