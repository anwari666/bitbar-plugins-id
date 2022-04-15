#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/bin/python3
# -*- coding: utf-8 -*-
# taken from Andrew Keating's transferwise module
# modified using python 3
# customised for indonesian formatting

import urllib.request
import json

# key availble from the old version of Transferwise's website
TRANSFERWISE_KEY = "dad99d7d8e52c2c8aaf9fda788d8acdc"

# Replace with desired currencies
currency_from = 'EUR'
currency_to = 'IDR'

url = "https://transferwise.com/api/v1/payment/calculate?amount=1" \
      "&amountCurrency=source&hasDiscount=false&isFixedRate=false" \
      "&isGuaranteedFixedTarget=false" \
      "&sourceCurrency={}&targetCurrency={}".format(currency_from, currency_to)

req = urllib.request.Request(url, headers={'X-Authorization-key': TRANSFERWISE_KEY})

# for BitBar
print("💰")
print("---")

resp = None

try: 
  resp = urllib.request.urlopen( req )

except:
  "tyda bisa konek :("

if resp is not None:
  result = json.loads(resp.read())['transferwiseRate']

  printout = f"{currency_from}/{currency_to} {result:,}"
  printout = printout.replace(',','#').replace('.',',').replace('#','.')
  
  print( printout )

else:
  print( "Cannot connect to TransferWise" )