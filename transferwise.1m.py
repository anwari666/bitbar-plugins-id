#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# -*- coding: utf-8 -*-
# taken from Andrew Keating's transferwise module
# modified using python 3
# customised for indonesian formatting

import urllib.request
import json

TRANSFERWISE_KEY = "dad99d7d8e52c2c8aaf9fda788d8acdc"

# Replace with desired currencies
currency_from = 'EUR'
currency_to = 'IDR'

url = "https://transferwise.com/api/v1/payment/calculate?amount=1" \
      "&amountCurrency=source&hasDiscount=false&isFixedRate=false" \
      "&isGuaranteedFixedTarget=false" \
      "&sourceCurrency={}&targetCurrency={}".format(currency_from, currency_to)

tw_req = urllib.request.Request(url, headers={'X-Authorization-key': TRANSFERWISE_KEY})

resp = None

try: 
  resp = urllib.request.urlopen( tw_req )

except:
  "tyda bisa konek :("

if resp is not None:
  result = json.loads(resp.read())['transferwiseRate']

  printout = f"{currency_from}/{currency_to} {result:,}"
  printout = printout.replace(',','#').replace('.',',').replace('#','.')
  
  print("💰")
  print("---")
  print( printout )

else:
  print( "gagal request ke transferwise" )