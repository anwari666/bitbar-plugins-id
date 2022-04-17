#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/bin/python3
# -*- coding: utf-8 -*-

# Fetch prayer times according to SalahHour.com API. 
# More info regarding calculation method, etc can be found under
# this page http://salahhour.com/index.php/api/index

import urllib.request
import json

# ------ SETTINGS -------
# Grab your latitude and longitude from Google Map
# by pinpointing any location, and you'll find those
# in the url with this format `@latitude,longitude` e.g @12.345,67.123

latitude  = -6.9034443
longitude = 107.5731168
timezone  = "Asia/Jakarta"
method    = 12 # 12 is from Sistem Informasi Hisab Rukyat Indonesia. 
# ------ END SETTINGS -------



def format_line(str):
  return str + "| trim=false | color=#FFFFFE"


def format_monospace(str):
  font="Monaco"
  return str + f" font={font}"


def main():
  url = "http://salahhour.com/index.php/api/prayer_times?latitude={}&longitude={}" \
        "&timezone={}&time_format=0&method={}" \
        "&maghrib_rule=1&maghrib_value=4" \
        .format(latitude, longitude, timezone, method)

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

    print( format_line(f"Jadwal solat hari ini"))
    print("---")
    
    print( format_monospace(format_line(f"Shubuh\t\t\t{fajr}" )))
    print( format_monospace(format_line(f"Dzuhur\t\t\t{dhuhr}" )))
    print( format_monospace(format_line(f"Asr\t\t\t\t{asr}" )))
    print( format_monospace(format_line(f"Maghrib\t\t\t{maghrib}" )))
    print( format_monospace(format_line(f"Isya\t\t\t{isha}" )))

  else:
    print( "Cannot connect to SalahHour API" )

# Actually run the app
main()