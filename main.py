from tkinter import *
from buttonbars import *
from Event import *
import data_handler
from datetime import date
import util as utils
from dailyview import renderCalendar
import datetime
from googleclient import authenticateGoogleCalendar
from reviewpopup import ReviewPopup

service = None

buttonbar = None
dailyView = None
weeklyView = None

# TIME FORMAT: HH:MM AM/PM
# Accepted times: 12:00 AM - 11:59 PM
# Holds the raw events
eventData = []

# Get date string: utils.toDateString(currentDate)
currentDate = datetime.datetime.today()

# Holds the events with the rows they're going to be displayed on
scheduledData = [[]]

eventData.append(
    Event("Discrete Test", "NFAs", "09-26-21", "11:00 AM", "1:00 PM", eventType="event"))
eventData.append(Event("Science Test", "Biology",
                 "9:00 AM", "3:00 PM", eventType="event", currentDate=currentDate))
eventData.append(Event("Science Test 2", "Biology 2",
                 "9:00 AM", "3:00 PM", eventType="event", currentDate=currentDate))
eventData.append(Event(
    "SS Project", "Finish our project - still waiting on Joe to notify", "8:45 AM", "11:15 AM", eventType="task", currentDate=currentDate))
eventData.append(Event("Programming Test Prep", "CS1",
                 "12:45 PM", "3:00 PM", eventType="task", currentDate=currentDate))
eventData.append(Event(
    "Math Test - VERY LONG NAME THAT WILL WRAP INTO LOTS OF LINES AND POTENTIALLY CAUSE LOTS OF PROBLEMS BUT HOPEFULLY WE CAN FIX THEM", "Calculus - Start of a really long description that we need to be able to wrap and limit. Can we make this even longer though and not break the text?", "8:45 AM", "9:45 AM", eventType="event", currentDate=currentDate))
eventData.append(Event("Hang out with Shelly", "Still haven't decided where we're going",
                       "7:00 PM", "11:59 PM", actualStart="8:00PM", actualEnd="11:59 PM", eventType="task", currentDate=currentDate))

data_handler.dump_event(eventData[0])

canvWidth = utils.canvWidth
canvHeight = utils.canvHeight
cellWidth = utils.cellWidth

canvStartHour = 0

def incStart():
    global canvStartHour, dailyView
    if canvStartHour >= 24 - canvWidth/cellWidth:
        return
    canvStartHour += 1
    rerenderCanvas()


def decStart():
    global canvStartHour, dailyView
    if canvStartHour == 0:
        return
    canvStartHour -= 1
    rerenderCanvas()


def incDate():
    global currentDate
    currentDate += datetime.timedelta(days=1)
    rerenderTopBar()
    # Swap out eventData (list of event objects) to load whatever JSON events are at the new currentDate value
    # toDateString(dateTime) for JSON keys
    # scheduleEvents()
    # rerenderCanvas()


def decDate():
    global currentDate
    currentDate -= datetime.timedelta(days=1)
    rerenderTopBar()


def updateEvent(newVersion):
    # Replace previous version with new version
    # Re-sort and re-render
    for i in range(0, len(eventData)):
        event = eventData[i]
        if event.uuid == newVersion.uuid:
            eventData[i] = newVersion

            # Save the JSON for the updated event in place of the existing event at the currentDate

            scheduleEvents()
            rerenderCanvas()
            return True
    return False  # Indicate it's safe to replace prevVersion with newVersion


def deleteEvent(previousVersion):
    # resort and render the calendar again
    for i in range(0, len(eventData)):
        event = eventData[i]
        if event.uuid == previousVersion.uuid:
            eventData.remove(event)

            # Delete the JSON object of the deleted event

            scheduleEvents()
            rerenderCanvas()
            return True
    return False


# Call every time an event gets added or removed
def scheduleEvents():
    eventData.sort()
    scheduledData.clear()
    for singleEvent in eventData:
        index = 0

        while True:
            if index >= len(scheduledData):
                scheduledData.append([])
                break
            elif len(scheduledData[index]) == 0:
                break
            else:
                previousEventEnd = scheduledData[index][len(
                    scheduledData[index]) - 1].end
                if(previousEventEnd.__le__(singleEvent.start)):
                    break

            index += 1

        scheduledData[index].append(singleEvent)


def addNewEvent(event):
    eventData.append(event)

    # Update the JSON object for the currentDate to include this new event

    scheduleEvents()
    rerenderCanvas()


def syncCalendar():
    global service

    if service is None:
        service = authenticateGoogleCalendar()

    startTime = datetime.datetime(
        currentDate.year, currentDate.month, currentDate.day, 0, 0, 0, 0).astimezone(tz=datetime.timezone.utc).isoformat()  # midnight today
    endTime = datetime.datetime(
        currentDate.year, currentDate.month, currentDate.day, 23, 59, 59, 0).astimezone(tz=datetime.timezone.utc).isoformat()  # 11:59PM today

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events_result = service.events().list(calendarId='primary', timeMin=startTime, timeMax=endTime, singleEvents=True,
                                          orderBy='startTime').execute()
    google_events_list = events_result.get('items', [])

    if not google_events_list:
        print('No upcoming events found.')

    print('Found ' + str(len(google_events_list)) + ' events')

    # Remove any google events that we're pulled previously so we don't introduce any duplicates
    i = 0
    while len(eventData) > i:
        e = eventData[i]
        print(e)
        if e.fromGoogle == True:
            print("Removing")
            eventData.remove(e)
        else:
            i += 1
        print(len(eventData))

    for e in google_events_list:
        name = e['summary']
        description = e['description'] if 'description' in e else e['htmlLink']
        start = datetime.datetime.fromisoformat(
            e['start'].get('dateTime', e['start'].get('date'))).replace(tzinfo=None)
        end = datetime.datetime.fromisoformat(
            e['end'].get('dateTime', e['end'].get('date'))).replace(tzinfo=None)

        # Remove any events that start/end on a different day, which are not currently supported by this application
        if start.date() != currentDate.date() or end.date() != currentDate.date():
            continue

        newEvent = Event(name, description, start, end,
                         fromGoogle=True, currentDate=currentDate)
        eventData.append(newEvent)
    scheduleEvents()
    rerenderCanvas()


def generateDailyReview():
    popup = ReviewPopup(currentDate, eventData,
                        scheduledData, frequency="daily")


def generateWeeklyReview():
    popup = ReviewPopup(currentDate, eventData,
                        scheduledData, frequency="weekly")


def rerenderTopBar():
    for child in topButtonBar.winfo_children():
        child.destroy()
    topButtonBar.pack(fill=X)
    renderTopBar(topButtonBar, currentDate,
                 (addNewEvent, syncCalendar, incDate, decDate))
    print("re-rendered top bar")


def rerenderCanvas():
    for child in dailyView.winfo_children():
        child.destroy()
    dailyView.pack()
    renderCalendar(dailyView, currentDate, scheduledData, canvStartHour,
                   (updateEvent, deleteEvent))


scheduleEvents()

window = Tk()
window.geometry("1500x1000")
window.resizable(0, 0)
window.configure(bg="white")
window.winfo_toplevel().title("Visualize Your Day")

topButtonBar = Frame(window, bd=5, bg="white")
topButtonBar.pack(fill=X)
rerenderTopBar()

dailyView = Frame(window)
dailyView.pack()
rerenderCanvas()

bottomButtonBar = Frame(window, bg="white")
bottomButtonBar.pack(fill=X)
renderBottomBar(bottomButtonBar, (incStart,
                decStart, generateDailyReview, generateWeeklyReview))

window.mainloop()
