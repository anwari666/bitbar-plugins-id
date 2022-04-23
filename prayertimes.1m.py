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

PAST_ISYA = "PAST_ISYA"

class TextFormatter:
  """Class to format the text's output"""
  
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



class TimeService:

  def __init__(self):
    self.now = datetime.datetime.now()
  
  
  def total_hours(self, seconds ):
    return int(seconds // 3600)

  
  def total_minutes(self, seconds ):
    return int(( seconds % 3600 ) // 60)

  
  def difference_in_seconds(self, later, newer): 
    return ( later - newer ).total_seconds()

  
  def remaining_hour(self, later, newer):
    return self.total_hours( self.difference_in_seconds( later, newer ) )

  
  def remaining_minutes(self, later, newer):
    return self.total_minutes( self.difference_in_seconds( later, newer ) )

  
  def format_time(self, num, hand):
    return f"{num} {hand} "  if num != 0 else ""

  
  def by_value(self, item):
    return item[1]



class PrayerTimeService(TimeService):
  """Class to deal with prayer timings"""

  def __init__(self, prayers):
    super().__init__()

    self.__prayers = prayers
    
    self.__next_prayer = None
    self.calc_next_prayer()
    
    self.__next_prayer_time = None
    self.calc_next_prayer_time()


  def calc_next_prayer(self):
    
    # iterate over (sorted) result
    for prayer_name, prayer_time in sorted(self.__prayers.items(), key=self.by_value):
      
    # while current time is smaller, continue until it's bigger.
      if prayer_name in PRAYER_TRANSLATION.keys():

        prayer_datetime = self.convert_24h_to_datetime(prayer_time)
        
        # Found the next one.
        if (prayer_datetime > self.now) :
          self.__next_prayer = prayer_name
          return

    # if not found, set default to past isya.
    self.__next_prayer = PAST_ISYA # "Isha"


  def get_next_prayer(self):
    return self.__next_prayer


  def get_next_prayer_time(self):
    return self.__next_prayer_time


  def calc_next_prayer_time(self):
    if ( self.__next_prayer != PAST_ISYA ):
      self.__next_prayer_time = self.convert_24h_to_datetime(self.__prayers[self.__next_prayer])


  def convert_24h_to_datetime(self, str):
    [hour, minute] = str.split(':')
    return datetime.datetime( int(self.now.year), 
                              int(self.now.month), 
                              int(self.now.day),
                              int(hour),
                              int(minute), 
                              0)


  def time_to_next_prayer(self):
    return self.format_time( self.remaining_hour( self.__next_prayer_time, self.now ), 'jam') + self.format_time(self.remaining_minutes(  self.__next_prayer_time, self.now  ), 'menit')



class PrintService:

  def print_info(self, prayers):
    
    print( TextFormatter(f"Jadwal solat hari ini").highlight().get() )

    prayer_times = PrayerTimeService(prayers)
    next_prayer = prayer_times.get_next_prayer()


    if (next_prayer != PAST_ISYA):
      next_time = prayer_times.get_next_prayer_time()
      info_text = TextFormatter(":arrow_right: " + PRAYER_TRANSLATION[next_prayer] + " dalam " + prayer_times.time_to_next_prayer() + " | emojize=true ")
      print( info_text.highlight().get() )
    
    print("---")


  def print_tables(self, prayers):
    for prayer_name, prayer_time in sorted(prayers.items(), key=TimeService().by_value):
      if prayer_name in PRAYER_TRANSLATION.keys():
        prayer_row_text = TextFormatter(f"{ PRAYER_TRANSLATION[prayer_name]:18} {prayer_time}" )
        print( prayer_row_text.monospace().highlight().get() )


  def print(self, prayers):
    self.print_info(prayers)
    self.print_tables(prayers)



class PrayerService:
  """
  Class to fetch prayers data. 
  Later will probably utilise sqlite to not always fetching the API every minute."""

  def fetch(self):
    """Fetch method will change based on whether there is cached data"""
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

    if response is not None:
      return json.loads(response.read())['results']

    return None



class App:
  """The actual app to invoke"""
  def main():
    
    print("🙏")
    print("---")

    prayers = PrayerService().fetch()

    if prayers is not None:
      PrintService().print(prayers)

    else:
      print( "Tidak dapat terhubung dengan internet" )

    return False


# Run the main function
App.main()