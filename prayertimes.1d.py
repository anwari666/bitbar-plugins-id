#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/bin/python3
# -*- coding: utf-8 -*-

# Fetch prayer times according to SalahHour.com API. 
# More info regarding calculation method, etc can be found under
# this page http://salahhour.com/index.php/api/index

import urllib.request
import json
import datetime

# ------ SETTINGS -------
# Grab your latitude and longitude from Google Map
# by pinpointing any location, and you'll find those
# in the url with this format `@latitude,longitude` e.g @12.345,67.123

latitude  = 41.176181
longitude = -8.584248
timezone  = "Europe/Lisbon"
method    = 3 # 12 is from Sistem Informasi Hisab Rukyat Indonesia. 
# ------ END SETTINGS -------

PRAYER_TRANSLATION = {
  "Fajr"    : "Shubuh",
  "Dhuhr"   : "Dzuhur",
  "Asr"     : "Ashar",
  "Maghrib" : "Magrib",
  "Isha"    : "Isya"
}

def format_line(str):
  return str + "| trim=false | color=#dddddd"


def format_monospace(str):
  font="Monaco"
  return str + f" font={font}"

def by_value(item):
  return item[1]

# get current time
def now():
  return datetime.datetime.now()

def isya():
  return datetime.datetime(2022, 4, 17, 19, 0, 0)

def next_prayer_time():
  # get current time
  # iterate over (sorted) result
  # while current time is smaller, continue until it's bigger.
  # you found it. Return that shit
  noop()

def convert_24h_to_datetime(str):
  [hour, minute] = str.split(':')
  return datetime.datetime( int(now().year), 
                            int(now().month), 
                            int(now().day),
                            int(hour),
                            int(minute), 
                            0)

def total_hours( seconds ):
  return int(seconds // 3600)

def total_minutes( seconds ):
  return int(( seconds % 3600 ) // 60)

def difference_in_seconds(later, newer): 
  return ( later - newer ).total_seconds()

def remaining_hour(later, newer):
  return total_hours( difference_in_seconds( later, newer ) )

def remaining_minutes(later, newer):
  return total_minutes( difference_in_seconds( later, newer ) )

def remaining_time(later, now):
  return format_time( remaining_hour( later, now ), 'jam') + format_time(remaining_minutes(  later, now  ), 'menit')

def format_time(num, hand):
  return f"{num} {hand} "  if num != 0 else ""

def main():
  url = "http://salahhour.com/index.php/api/prayer_times?latitude={}&longitude={}" \
        "&timezone={}&time_format=0&method={}" \
        "&maghrib_rule=1&maghrib_value=4" \
        .format(latitude, longitude, timezone, method)

  req = urllib.request.Request(url)

  resp = None

  try: 
    resp = urllib.request.urlopen( req )

  except:
    "tyda bisa konek :("

  if resp is not None:
    
    print( format_line(f"Jadwal solat hari ini"))
    print("---")

    prayers = json.loads(resp.read())['results']

    found_next = ''
    # now = now()
    
    for prayer_name, prayer_time in sorted(prayers.items(), key=by_value):
      
      if prayer_name in PRAYER_TRANSLATION.keys():

        prayer_datetime = convert_24h_to_datetime(prayer_time)
        
        if ((prayer_datetime > now()) and (found_next == '')) :
          found_next = prayer_name
          print( format_line(PRAYER_TRANSLATION[prayer_name] + " dalam " + remaining_time(prayer_datetime, now())))
          
    print("---")

    for prayer_name, prayer_time in sorted(prayers.items(), key=by_value):
      if prayer_name in PRAYER_TRANSLATION.keys():
        print( format_monospace(format_line(f"{ PRAYER_TRANSLATION[prayer_name]:16} {prayer_time}" )))


  else:
    print( "Cannot connect to SalahHour API" )

print("🙏")
print("---")
#print( f"Isya dalam { remaining_time() }" )

# Actually run the app
main()