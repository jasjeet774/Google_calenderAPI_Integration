from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
scopes=['https://www.googleapis.com/auth/calendar']
flow=InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
Credentials=flow.run_local_server()
# print(Credentials)
# for save credentials
import pickle
pickle.dump(Credentials,open("token.pkl","wb"))
credentials=pickle.load(open("token.pkl","rb"))


service=build("calendar","v3",credentials=credentials)

# get calendar
result=service.calendarList().list().execute()
# print(result)
print(result['items'][1])

#  get events
calendar_id=result['items'][1]['id']
result=service.events().list(calendarId=calendar_id,timeZone="Asia/kolkata").execute()

print(result['items'][-1])

# create a calendar event

from datetime import datetime,timedelta
start_time=datetime(2023,9,2,3,0,0)
end_time=start_time+timedelta(hours=4)
timezone='Asia/Kolkata'

event = {
  'summary': 'Aisa cup IND?PAk 3pm',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
    'timeZone': timezone,
  },
  'end': {
    'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
    'timeZone': timezone,
  },
  'attendees': [
    {'email': 'vinayguggi136@gmail.com'}
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

event = service.events().insert(calendarId=calendar_id, body=event).execute()

import datefinder
matches=datefinder.find_dates("31 aug 10 PM")
list(matches)


def create_event(start_time_str, summary, duration=1, description=None, location=None):
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId='primary', body=event).execute()

create_event("2 september 2 pm","meeting")
