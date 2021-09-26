from datetime import datetime
from tkinter import Widget
from Event import *
import shortuuid
import json


def timeString(date: datetime.datetime):
    return date.strftime("%m-%d-%-y")

# # TODO: make functions for creating Event object from JSON
# def load_event(title, description, start="12:00 AM", end="12:01 AM", actualStart=None, actualEnd=None, eventType="event"):
#     return Event(title, description, start, end, actualStart, actualEnd, eventType)

def loadDayEvents(date: datetime.datetime):
    with open('event_data.json', 'r') as in_file:
        data = json.load(in_file)

    try:
        return data[timeString(date)]
    except:
        data[timeString(date)] = {}
        return {}

# to the data file
def dumpEvent(event: Event):
    export_event = {
            "name": event.name,
            "description": event.description,
            "eventType": event.eventType,
            "start": event.start.timeString,
            "end": event.end.timeString,
            "actualStart": event.actualStart.timeString,
            "actualEnd": event.actualEnd.timeString
        }

    with open('event_data.json', 'r') as in_file:
        data = json.load(in_file)

    try:
        data[event.currentDate][shortuuid.uuid()]
    except KeyError:
        data[event.currentDate] = {}
    data[event.currentDate][shortuuid.uuid()] = export_event

    with open('event_data.json', 'w') as out_file:
        json.dump(data, out_file, indent=2)

def new_event(title, description, start="12:00 AM", end="12:01 AM", actualStart=None, actualEnd=None, eventType="event"):
    uuid = shortuuid.uuid()

# loads event from the data file to edit and save back to the data file
def edit_event():
    pass

# deletes event from the data file
def delete_event():
    pass
