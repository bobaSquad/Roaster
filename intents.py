from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dateutil.parser import parse
from datetime import timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']


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

