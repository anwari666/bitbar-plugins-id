#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/bin/python3
# -*- coding: utf-8 -*-

# Fetch prayer times according to SalahHour.com API. 
# More info regarding calculation method, etc can be found under
# this page http://salahhour.com/index.php/api/index

import urllib.request
import json
import datetime

# ====== SETTINGS ======
# Grab your latitude and longitude from Google Map
# by pinpointing any location, and you'll find those
# in the url with this format `@latitude,longitude` e.g @12.345,67.123

latitude  = 41.176181
longitude = -8.584248
timezone  = "Europe/Lisbon"
method    = 3 # 12 is from Sistem Informasi Hisab Rukyat Indonesia. 
# ====== END SETTINGS ======

PRAYER_TRANSLATION = {
  "Fajr"    : "Shubuh",
  "Dhuhr"   : "Dzuhur",
  "Asr"     : "Ashar",
  "Maghrib" : "Magrib",
  "Isha"    : "Isya"
}

class TextFormatter:
  __text = ''

  def __init__(self, txt):
    self.__text = txt

  def highlight(self):
    self.__text += "| href=# "
    return self

  def monospace(self):
    font="Monaco"
    self.__text += f"| font={font} "
    return self

  def get(self):
    return self.__text


def by_value(item):
  return item[1]

# get current time
def now():
  return datetime.datetime.now()

def next_prayer_time(prayers):
  # get current time
  found_next = False
  
  # iterate over (sorted) result
  for prayer_name, prayer_time in sorted(prayers.items(), key=by_value):
    
  # while current time is smaller, continue until it's bigger.
    if prayer_name in PRAYER_TRANSLATION.keys():

      prayer_datetime = convert_24h_to_datetime(prayer_time)
      
      # you found it. Return that.
      if ((prayer_datetime > now()) and not found_next ) :
        return prayer_name

  return "past isya"


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

def print_info(prayers):
  
  print( TextFormatter(f"Jadwal solat hari ini coy").highlight().get() )

  next_prayer = next_prayer_time(prayers)
  next_time = convert_24h_to_datetime(prayers[next_prayer])
  
  print( TextFormatter(":soon: " + PRAYER_TRANSLATION[next_prayer] + " dalam " + remaining_time(next_time, now()) + " | emojize=true ").highlight().get() )
  print("---")

def print_tables(prayers):
  for prayer_name, prayer_time in sorted(prayers.items(), key=by_value):
    if prayer_name in PRAYER_TRANSLATION.keys():
      print( TextFormatter(f"{ PRAYER_TRANSLATION[prayer_name]:18} {prayer_time}" ).monospace().highlight().get() )

def print_prayers(prayers):
  print_info(prayers)
  print_tables(prayers)


def fetch_prayers():
  url = "http://salahhour.com/index.php/api/prayer_times?latitude={}&longitude={}" \
        "&timezone={}&time_format=0&method={}" \
        "&maghrib_rule=1&maghrib_value=4" \
        .format(latitude, longitude, timezone, method)

  req = urllib.request.Request(url)

  response = None

  try: 
    response = urllib.request.urlopen( req )

  except:
    "tyda bisa konek :("

  return response


def main():
  response = fetch_prayers()

  if response is not None:
    prayers = json.loads(response.read())['results']
    print_prayers(prayers)

  else:
    print( "Tidak dapat terhubung dengan internet" )

  return False



# Start from here
print("🙏")
print("---")

# Actually run the app
main()