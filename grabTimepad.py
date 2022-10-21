from creds import *

import requests
import datetime


def get_events(ids):
  if type(ids) == list:
    org_ids = ','.join(str(id) for id in ids)
  else: 
    org_ids = str(ids)

  dateNow = str(datetime.date.today())

  url = f'{API_TIMEPAD_URL}.json'
  plFields = ['id',
              'location',
              'description_short',
              'description_html',
              'organization',
              'moderation_statuses',
              'tickets_limit'
              ]

  payload = {
  'show_empty_fields':'false', 
  'fields':plFields , 
  'limit':'20' , 
  'organization_ids':f'{org_ids}',
  'starts_at_min':f'{dateNow}'
  }

  r = requests.get(url, params=payload, headers={'Authorization': f'Bearer {API_TIMEPAD_TOKEN}'})
  response = r.json()
  
  def customSort(e):
    return e['starts_at']

  response['values'].sort(key=customSort)

  return response


def get_datesNames(response):
  # get dates and names of events in a dict
  answer = {}

  for event in response['values']:
    date = datetime.datetime.strptime(event['starts_at'], '%Y-%m-%dT%H:%M:%S+0300')
    answer[event['id']] = [event['name'], date]

  return answer


def get_orders(event_id): 
  # in: int // out: tuple
  url = f'{API_TIMEPAD_URL}/{event_id}/orders'
  plFields = ['id',
              'created_at',
              'status',
              'mail',
              'payment',
              'tickets',
              'answers',
              'promocodes',
              'event',
              'referrer',
              'subscribed_to_newsletter'
              ]

  payload = {'limit':'100', 'skip':'0' , 'event_id':f'{event_id}'}

  r = requests.get(url, params=payload, headers={'Authorization': f'Bearer {API_TIMEPAD_TOKEN}'})
  response = r.json()

  numOrders = response['total']
  numTickets = 0
  if numOrders == 0:
    pass
  else: 
    for order in response['values']:
      ticketsInOrder = len(order['tickets'])
      numTickets += ticketsInOrder

  return numOrders, numTickets
