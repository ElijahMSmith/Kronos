from datetime import datetime
from tkinter import Widget
from util import toDateString, getTimeString
from Event import *
import shortuuid
import json


def loadDayEvents(date: datetime.datetime):
    with open('event_data.json', 'r') as in_file:
        allData = json.load(in_file)

        try:
            loadData = allData[toDateString(date)]['events']
            retData = []
            for obj in loadData:
                retData.append(
                    Event(name=obj["name"], description=obj["description"], start=obj["start"], end=obj["end"], actualStart=obj["actualStart"], actualEnd=obj["actualEnd"], eventType=obj["eventType"], fromGoogle=obj["fromGoogle"], existingUUID=obj["existingUUID"]))
            return retData
        except:
            return []


def updateJSON(event: Event, currentDate):
    export_event = {
        "existingUUID": event.uuid,
        "name": event.name,
        "description": event.description,
        "eventType": event.eventType,
        "start": getTimeString(event.start),
        "end": getTimeString(event.end),
        "actualStart": getTimeString(event.actualStart),
        "actualEnd": getTimeString(event.actualEnd),
        "fromGoogle": event.fromGoogle,
    }

    with open('event_data.json', 'r') as in_file:
        data = json.load(in_file)

        if not (toDateString(currentDate) in data):
            data[toDateString(currentDate)] = {"events": []}

        eventObjects = data[toDateString(currentDate)]['events']

        for obj in eventObjects:
            print(obj)
            print(export_event)
            if obj["existingUUID"] == export_event["existingUUID"]:
                eventObjects.remove(obj)
                eventObjects.append(export_event)
                break

        with open('event_data.json', 'w') as out_file:
            json.dump(data, out_file, indent=4)


def new_event(event, currentDate):
    export_event = {
        "existingUUID": event.uuid,
        "name": event.name,
        "description": event.description,
        "eventType": event.eventType,
        "start": getTimeString(event.start),
        "end": getTimeString(event.end),
        "actualStart": getTimeString(event.actualStart),
        "actualEnd": getTimeString(event.actualEnd),
        "fromGoogle": event.fromGoogle,
    }

    with open('event_data.json', 'r') as in_file:
        data = json.load(in_file)

        if not (toDateString(currentDate) in data):
            data[toDateString(currentDate)] = {"events": []}

        eventObjects = data[toDateString(currentDate)]['events']
        eventObjects.append(export_event)

        with open('event_data.json', 'w') as out_file:
            json.dump(data, out_file, indent=4)


def delete_event(event, currentDate):
    matchUUID = event.uuid

    with open('event_data.json', 'r') as in_file:
        data = json.load(in_file)

    if not (toDateString(currentDate) in data):
        return

    print("pre-del", data)
    eventObjects = data[toDateString(currentDate)]['events']
    for obj in eventObjects:
        if obj["existingUUID"] == matchUUID:
            print("found")
            eventObjects.remove(obj)
            break
    print("post-del", data)

    with open('event_data.json', 'w') as out_file:
        json.dump(data, out_file, indent=4)
