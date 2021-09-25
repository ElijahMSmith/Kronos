from tkinter import *
from dailyview import *
from buttonbar import *
from Event import *
from datetime import date
from util import constants

buttonbar = None
dailyView = None
weeklyView = None

# TIME FORMAT: HH:MM AM/PM
# Holds the raw events
eventData = []

# Holds the events with the rows they're going to be displayed on
scheduledData = [[]]

eventData.append(
    Event("Discrete Test", "NFAs", "11:00 AM", "1:00 PM"))
eventData.append(Event("Science Test", "Biology", "9:00 AM", "3:00 PM"))
eventData.append(Event("Science Test 2", "Biology 2", "9:00 AM", "3:00 PM"))
eventData.append(Event("Math Test", "Calculus", "8:45 AM", "9:45 AM"))
eventData.append(Event("History Test", "SS", "8:45 AM", "11:15 AM"))
eventData.append(Event("Programming Test", "CS1", "12:45 PM", "3:00 PM"))
eventData.append(Event("Health Test", "Alcoholism", "7:00 PM", "11:59 PM"))

canvWidth = constants["canvWidth"]
canvHeight = constants["canvHeight"]
cellWidth = constants["cellWidth"]

canvStartHour = 0


def incStart():
    global canvStartHour, dailyView
    if canvStartHour >= 24 - canvWidth/cellWidth:
        return
    canvStartHour += 1

    for child in dailyView.winfo_children():
        child.destroy()

    dailyView.pack()
    renderCalendar(dailyView, scheduledData, canvStartHour)


def decStart():
    global canvStartHour, dailyView
    if canvStartHour == 0:
        return
    canvStartHour -= 1

    for child in dailyView.winfo_children():
        child.destroy()

    dailyView.pack()
    renderCalendar(dailyView, scheduledData, canvStartHour)


# Call every time an event gets added or removed
def scheduleEvents():
    eventData.sort()
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
        print("index = " + str(index) + singleEvent.__str__())


def newEvent():
    return


def syncCalendar():
    return


scheduleEvents()

window = Tk()
window.geometry("1500x1000")
window.resizable(0, 0)
window.configure(bg="white")
window.winfo_toplevel().title("Visualize Your Day")

topButtonBar = Frame(window, bd=5, bg="white")
topButtonBar.pack()
renderTopBar(topButtonBar, newEvent, syncCalendar)

dailyView = Frame(window, )
dailyView.pack()
renderCalendar(dailyView, scheduledData, canvStartHour)

bottomButtonBar = Frame(window, bg="white")
bottomButtonBar.pack(side=LEFT)
renderBottomBar(bottomButtonBar, incStart,
                decStart)

window.mainloop()
