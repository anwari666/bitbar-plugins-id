#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/bin/python3
# -*- coding: utf-8 -*-
# Fetch prayer times according to SalahHour.com API

import urllib.request
import json

# CHANGE YOUR SETTINGS HERE

latitude=41.176181
longitude=-8.584248
timezone="Europe/Lisbon"

font="Monaco"


url = "http://salahhour.com/index.php/api/prayer_times?latitude={}&longitude={}" \
      "&timezone={}&time_format=0&method=3&maghrib_rule=1&maghrib_value=4".format(latitude, longitude, timezone)

print(url)

req = urllib.request.Request(url)

print("🙏")
print("---")

resp = None

try: 
  resp = urllib.request.urlopen( req )

except:
  "tyda bisa konek :("

if resp is not None:
  result = json.loads(resp.read())['results']
  asr = result['Asr']
  dhuhr = result['Dhuhr']
  maghrib = result['Maghrib']
  isha = result['Isha']
  fajr = result['Fajr']

  print( f"Jadwal solat hari ini")
  print("---")
  
  print( f"Shubuh\t\t{fajr}|trim=false font={font}" )
  print( f"Dzuhur\t\t{dhuhr}|trim=false font={font}" )
  print( f"Asr\t\t\t{asr}|trim=false font={font}" )
  print( f"Maghrib\t\t{maghrib}|trim=false font={font}" )
  print( f"Isya\t\t{isha}|trim=false font={font}" )

else:
  print( "Cannot connect to SalahHour" )