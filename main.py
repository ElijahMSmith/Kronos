from tkinter import *
from buttonbars import *
from Event import *
from datetime import date
import util as utils
from dailyview import renderCalendar
import datetime

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
    Event("Discrete Test", "NFAs", "11:00 AM", "1:00 PM", eventType="event"))
eventData.append(Event("Science Test", "Biology",
                 "9:00 AM", "3:00 PM", eventType="event"))
eventData.append(Event("Science Test 2", "Biology 2",
                 "9:00 AM", "3:00 PM", eventType="event"))
eventData.append(Event(
    "SS Project", "Finish our project - still waiting on Joe to notify", "8:45 AM", "11:15 AM", eventType="task"))
eventData.append(Event("Programming Test Prep", "CS1",
                 "12:45 PM", "3:00 PM", eventType="task"))
eventData.append(Event(
    "Math Test - VERY LONG NAME THAT WILL WRAP INTO LOTS OF LINES AND POTENTIALLY CAUSE LOTS OF PROBLEMS BUT HOPEFULLY WE CAN FIX THEM", "Calculus - Start of a really long description that we need to be able to wrap and limit. Can we make this even longer though and not break the text?", "8:45 AM", "9:45 AM", eventType="event"))
eventData.append(Event("Hang out with Shelly", "Still haven't decided where we're going",
                       "7:00 PM", "11:59 PM", actualStart="8:00PM", actualEnd="11:59 PM", eventType="task"))

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


def decDate():
    global currentDate
    currentDate -= datetime.timedelta(days=1)
    rerenderTopBar()


def updateEvent(previousVersion, newVersion):
    # Replace previous version with new version
    # Re-sort and re-render
    for i in range(0, len(eventData)):
        event = eventData[i]
        if event.fullyEqual(previousVersion):
            eventData[i] = newVersion
            scheduleEvents()
            rerenderCanvas()
            return True

    return False  # Indicate it's safe to replace prevVersion with newVersion


def deleteEvent(previousVersion):
    # resort and render the calendar again
    for i in range(0, len(eventData)):
        event = eventData[i]
        if event.fullyEqual(previousVersion):
            eventData.remove(event)
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
    scheduleEvents()
    rerenderCanvas()


def syncCalendar():
    return


def rerenderTopBar():
    for child in topButtonBar.winfo_children():
        child.destroy()
    topButtonBar.pack(fill=X)
    renderTopBar(topButtonBar, currentDate,
                 (addNewEvent, syncCalendar, incDate, decDate))
    # rerenderCanvas()
    print("re-rendered top bar")


def rerenderCanvas():
    for child in dailyView.winfo_children():
        child.destroy()
    dailyView.pack()
    renderCalendar(dailyView, scheduledData, canvStartHour,
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
bottomButtonBar.pack(side=LEFT)
renderBottomBar(bottomButtonBar, incStart,
                decStart)

window.mainloop()
