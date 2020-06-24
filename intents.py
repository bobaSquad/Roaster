from __future__ import print_function
import datetime
import requests
import pickle
import urllib.parse
import os.path
import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# from dateutil.parser import parse
# from datetime import timedelta
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from dateutil.parser import parse
from datetime import timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']
KEY = "AIzaSyBDTle_FAUDLrCY2f5fpVrp1-DWfVvNeuY"


def get_events(cal_id, url, message_req):
    """
    Creates a REST request for calendar API to get upcoming 10 events and
    schedules reminders accordingly
    """
    # REST request
    URI = f'https://content.googleapis.com/calendar/v3/calendars/' \
          f'{urllib.parse.quote(cal_id)}/events' \
          f'?key={KEY}' \
          f'&maxResults=10' \
          f'&singleEvents=true' \
          f'&fields=items(summary%2Cstart)' \
          f'&timeMin={datetime.datetime.utcnow().isoformat()}Z'
    response = requests.get(URI).json()["items"]  # retrieving events
    scheduler = Scheduler("randomseed", connection=Redis())  # constructs
    # scheduler
    # with cal_id as identifier
    for event in response:
        st_time = datetime.datetime.strptime(f'{event["start"]["dateTime"]}Z',
                          '%Y-%m-%dT%H:%M:%SZ')
        message_req["message"]["text"] = f"Are you trying to fail this " \
                                         f"class!? SMH - {event.summary} is " \
                                         f"coming up!"
        scheduler.enqueue_at(st_time, requests.post(url=url, json=message_req))





def gethomework():
    # If modifying these scopes, delete the file token.pickle.
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return ("No", 'No upcoming events found')
    text=''
    print(events)
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        text=text+start+' '+event['summary']+'\n'
    #return(start, event['summary'])
    print(text)
    return('yes',text)


def addhomework(param):

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    homeworktype = param['homework']
    email = param['email']
    datehw = param['date']
    timehw = param['time']
    print(homeworktype, email, datehw, timehw)
    dt = parse(datehw)
    print(dt.date())
    datehw = str(dt.date())
    timehw = parse(timehw)
    timehw = str(timehw.time())
    ans = datehw+"T"+timehw+'+08:00'
    print(ans)
    dateu = parse(ans)
    newdate = dateu+timedelta(hours=1)
    newdate = str(newdate)
    newdate = parse(newdate)
    newdate = str(newdate.date())+"T"+str(newdate.time())+"+08:00"
    print(newdate, "HAHA")

    event = {
        'summary': homeworktype,
        'start': {
            'dateTime': ans,
            'timeZone': 'Asia/Singapore',
        },
        'end': {
            'dateTime': newdate,
            'timeZone': 'Asia/Singapore',
        },
        'attendees': [
            {'email': email},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId=email, body=event).execute()
    return {'fulfillmentText': homeworktype+' at' + datehw +' has been added to your calendar START WORKING U PIECE OF ****'}
    # print 'Event created: %s' % (event.get('htmlLink'))


if __name__ == '__main__':
    get_events("ag9126@g.rit.edu")