#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,cgi,cgitb
import json
import utr
cgitb.enable()

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
    monitor_info = utr.getmonitorcounts(apikey, ignore_paused)

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
  sys.stdout.write('{"frames":[{"text":"' + str(error) + '","icon":"i23080"}]}')
else:
  output = {}
  output['frames'] = []

  upout = {}
  upout['text'] = str(up) + ' ↑'
  upout['icon'] = 'i23079'
  output['frames'].append(upout)

  if down > 0:
    downout = {}
    downout['text'] = str(down) + ' ↓'
    downout['icon'] = 'i23080'
    output['frames'].append(downout)

  if paused > 0:
    pausedout = {}
    pausedout['text'] = str(paused) + ' II'
    pausedout['icon'] = 'i23081'
    output['frames'].append(pausedout)
   

  if unknown > 0:
    unknownout = {}
    unknownout['text'] = str(unknown) + ' ???'
    unknownout['icon'] = 'i23081'
    output['frames'].append(unknownout)

  sys.stdout.write(json.dumps(output))

