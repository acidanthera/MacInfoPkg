#!/usr/bin/env python

"""
Check and store product information

Relevant links:
http://support-sp.apple.com/sp/index?page=cpuspec&cc=XXXX
http://support-sp.apple.com/sp/product?cc=XXXX

Interesting examples:
-  01P - three character
- J094 - missing name
- J6FL - unicode
"""

import argparse
import datetime
import json
import os
import urllib2
import random
import signal
import sys
import time
import xml.etree.ElementTree
import yaml

STATUS_OK        = 'ok'
STATUS_PENDING   = 'pending'
STATUS_EXCEPT    = 'except'
STATUS_NOT_FOUND = 'not found'

valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
               'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def current_date():
  return time.mktime(datetime.datetime.now().date().timetuple())

def base34_to_num(str):
    num = 0
    for i in str:
      num *= 34
      num += valid_chars.index(i)
    return num

def num_to_base34(num):
    str = ''
    while num > 0:
      num, r = divmod(num, 34)
      str    = valid_chars[r] + str
    return str.zfill(3)

def load_products(path='Products.json'):
  try:
    with open(path, 'r') as fh:
      if path.endswith('.json'):
        return json.load(fh)
      else:
        db = yaml.safe_load(fh)
        for entry in db:
          db[entry]['date'] = time.mktime(db[entry]['date'].timetuple())
        return db
  except IOError:
    return {}
  except Exception as e:
    print("Failed to parse file %s - %s" % (path, e))
    sys.exit(1)

def save_database(database, path='Products.json'):
  # We are not using yaml for speed reasons.
  with open(path, 'w') as fh:
    json.dump(database, fh, indent=0, separators=(',', ':'), sort_keys=True)

def store_product(database, model, name, exception, status, date = None):
  database[model] = {
    'name': name,
    'except': exception,
    'status': status,
    'date': current_date() if date is None else date
  }

def update_product(database, model, force = False, retention = 90):
  prev = database.get(model, None)

  if prev is not None:
    if force is False and prev['status'] == STATUS_OK:
      print(u'{} - {} (skip)'.format(model, prev['name']))
      return

    curr   = current_date()
    expire = prev['date'] + retention*24*3600
    if expire > curr and prev['status'] == STATUS_NOT_FOUND:
      print(u'{} - not found (skip {})'.format(model, datetime.date.fromtimestamp(prev['date'])))
      return

    expire = prev['date'] + retention*24*3600 / 2
    if expire > curr and prev['status'] == STATUS_PENDING:
      print(u'{} - pending (skip {})'.format(model, datetime.date.fromtimestamp(prev['date'])))
      return

  try:
    url    = 'http://support-sp.apple.com/sp/product?cc={}'.format(model)
    opener = urllib2.build_opener()
    mm     = random.choice(range(11, 16))
    ff     = random.choice(range(50, 70))
    agent  = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.{}; rv:{}) Gecko/20100101 Firefox/{}'.format(mm, ff, ff)
    opener.addheaders = [
      ('Host', 'support-sp.apple.com'),
      ('User-Agent', agent),
      ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
      ('Accept-Language', 'en-US,en;q=0.5'),
      ('Accept-Encoding', 'gzip, deflate, br'),
      ('DNT', '1'),
      ('Connection', 'keep-alive'),
      ('Upgrade-Insecure-Requests', '1'),
      ('Cache-Control', 'max-age=0'),
    ]
    response = opener.open(url)
    root     = xml.etree.ElementTree.fromstring(response.read())
  except Exception as e:
    print(u'{} - except ({})'.format(model, str(e)))
    store_product(database, model, None, str(e), STATUS_EXCEPT)
    time.sleep(1)
    return

  if root.find('error') is None and root.find('configCode') is not None:
    name   = root.find('configCode').text
    status = STATUS_OK if name is not None else STATUS_PENDING
    print(u'{} - {}'.format(model, name))
    store_product(database, model, name, None, status)
    save_database(database) # Always store valid product
  else:
    print(u'{} - not found'.format(model))
    store_product(database, model, None, None, STATUS_NOT_FOUND)

def merge_products(database, filename):
  print('Merging {}'.format(filename))

  if not os.path.exists(filename):
    print(u'File {} is missing'.format(filename))
    sys.exit(1)

  new_database = load_products(filename)

  for model in new_database:
    new = new_database[model]
    old = database.get(model, None)
    store = False
    if old is None:
      store = True
    elif old != new:
      if old['status'] == new['status'] and old['name'] == new['name'] and old['except'] == new['except']:
        store = new['date'] > old['date']  # Update date if newer
      elif old['status'] != 'ok' and new['date'] > old['date']:
        store = True # Update new status
      else:
        print(u'Skipping {} entry for {}'.format(str(old), str(new)))

    if store:
      store_product(database, model, new['name'],
        new['except'], new['status'], new['date'])

  save_database(database)

def update_products(database, start_from, end_with, force = False, retention = 45, savenum = 512):
  start     = base34_to_num(start_from)
  end       = base34_to_num(end_with)
  countdown = savenum
  while start <= end:
    update_product(database, num_to_base34(start), force)
    start += 1
    if countdown == 0:
      save_database(database)
      countdown  = savenum
    else:
      countdown -= 1

  save_database(database)

def main():
  parser = argparse.ArgumentParser(description='Update product database')
  parser.add_argument('start', default='000', nargs='?', help='Starting product ID')
  parser.add_argument('end', default='ZZZZ', nargs='?', help='Ending product ID')
  parser.add_argument('--force', action='store_true', help='Recheck all products')
  parser.add_argument('--retention', type=int, default=90, help='Check products older than N days')
  parser.add_argument('--savenum', type=int, default=512, help='Save every N products while invalid')
  parser.add_argument('--merge', type=str, default=None, help='Merge specified database DB into main')

  args = parser.parse_args()

  db = load_products()
  
  if args.merge is not None:
    return merge_products(db, args.merge)

  for id in [args.start, args.end]:
    if len(id) < 3 or len(id) > 4:
      print(u'Invalid length for ID {}'.format(id))
      sys.exit(1)

    if not set(id) < set(valid_chars):
      print(u'Invalid characters in ID {}'.format(id))
      sys.exit(1)

  def abort_save_database(sig, frame):
    print('Aborting with database save on SIGINT!')
    save_database(db)
    sys.exit(0)

  signal.signal(signal.SIGINT, abort_save_database)

  return update_products(db, args.start, args.end, args.force, args.retention, args.savenum)

if __name__ == '__main__':
  main()
