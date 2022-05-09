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

latitude  = -6.9034443
longitude = 107.5731168
timezone  = "Asia/Jakarta"
method    = 12 # 12 is from Sistem Informasi Hisab Rukyat Indonesia. 

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
  """Class to format the text's output
  based on xbar's formatting with pipes """

  def __init__(self, txt):
    self.__text = txt

  def highlight(self):
    self.__text += "| href=# "
    return self

  def small(self):
    self.__text += "| size=12 "
    return self

  def monospace(self):
    font = "Monaco"
    self.__text += f"| font={font} "
    return self

  def get(self):
    return self.__text


class TimeService:

  @staticmethod
  def now():
    return datetime.datetime.now()

  @staticmethod
  def total_hours(seconds):
    if (seconds >= 0):
      return int(seconds // 3600)
    raise ValueError('Parameter must be greater than 0 seconds')

  @staticmethod
  def total_minutes(seconds):
    return int((seconds % 3600) // 60)

  @staticmethod
  def difference_in_seconds(later, newer):
    return (later - newer).total_seconds()

  @staticmethod
  def format_time(num, hand):
    return f"{num} {hand} " if num != 0 else ""

  def remaining_hour(self, seconds):
    return self.total_hours(seconds)

  def remaining_minutes(self, seconds):
    return self.total_minutes(seconds) + 1
  
  def convert_24h_to_datetime(self, str):
    [hour, minute] = str.split(':')
    now = self.now()
    return datetime.datetime( int(now.year), 
                              int(now.month),
                              int(now.day),
                              int(hour),
                              int(minute),
                              0)

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
        if (prayer_datetime > self.now()):
          self.__next_prayer = prayer_name
          return

    # if not found, set default to past isya.
    self.__next_prayer = PAST_ISYA  # "Isha"

  def get_next_prayer(self):
    return self.__next_prayer

  def get_next_prayer_time(self):
    return self.__next_prayer_time

  def calc_next_prayer_time(self):
    if (self.__next_prayer != PAST_ISYA):
      next_prayer_hour        = self.__prayers[self.__next_prayer]
      self.__next_prayer_time = self.convert_24h_to_datetime(next_prayer_hour)

  def time_to_next_prayer(self):
    now               = self.now()
    seconds_diff      = self.difference_in_seconds(self.__next_prayer_time, now)
    remaining_hour    = self.remaining_hour(seconds_diff)
    remaining_minutes = self.remaining_minutes(seconds_diff)
    return self.format_time(remaining_hour, 'jam') + self.format_time(remaining_minutes, 'menit')


class PrintService:

  def __init__(self, prayers):
    self.__prayers = prayers

  def print_info(self):
    header_text   = TextFormatter(f"Jadwal solat hari ini")
    prayer_times  = PrayerTimeService(self.__prayers)
    next_prayer   = prayer_times.get_next_prayer()

    if (next_prayer != PAST_ISYA):
      print(header_text.small().get())

      info_text = TextFormatter(
          ":arrow_right: " + PRAYER_TRANSLATION[next_prayer] + " dalam " + prayer_times.time_to_next_prayer() + " | emojize=true ")
      print(info_text.highlight().get())

    else:
      print(header_text.get())

    print("---")

  def print_tables(self):
    for prayer_name, prayer_time in sorted(self.__prayers.items(), key=TimeService().by_value):
      if prayer_name in PRAYER_TRANSLATION.keys():
        prayer_row_text = TextFormatter(
            f"{ PRAYER_TRANSLATION[prayer_name]:18} {prayer_time}")
        print(prayer_row_text.monospace().highlight().get())

  def print(self):
    self.print_info()
    self.print_tables()


class PrayerService:
  """
  Class to fetch prayers data. 
  Later will probably utilise sqlite to not always fetching the API every minute."""

  @classmethod
  def fetch(cls):
    """Fetch method will change based on whether there is cached data"""
    url = "http://salahhour.com/index.php/api/prayer_times?latitude={}&longitude={}" \
          "&timezone={}&time_format=0&method={}" \
          "&maghrib_rule=1&maghrib_value=4" \
          .format(latitude, longitude, timezone, method)

    req = urllib.request.Request(url)

    response = None

    try:
      response = urllib.request.urlopen(req)

    except urllib.error.HTTPError as e:
      print('Tyda bisa konek :(... Error code: ', e.code)

    except urllib.error.URLError as e:
      print('Tyda bisa konek :(... Reason: ', e.reason)

    if response is not None:
      return json.loads(response.read())['results']

    return None


class App:
  """The actual app to invoke"""

  @classmethod
  def main(cls):
    print("🙏")
    print("---")

    prayers = PrayerService.fetch()

    if prayers is not None:
      PrintService(prayers).print()

    else:
      print("Tidak dapat terhubung dengan internet")

    return False


if (__name__ == "__main__"):
  # Run the main function
  App.main()
