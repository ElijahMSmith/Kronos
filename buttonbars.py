from tkinter import *
from tkinter.font import Font
from Event import *
from neweventview import *
from util import toDateString
import datetime

addNewEventCallback = None
popup = None


def openNewEventPopup():
    global popup
    if not(popup is None) and not (popup.win is None):
        popup.win.destroy()
    popup = NewEventPopupWindow(addNewEventCallback)


def renderTopBar(frame, currentDate, callbacks):
    global addNewEventCallback
    buttonText = Font(frame, size=15)
    addNewEventCallback = callbacks[0]
    syncWithCalendar = callbacks[1]
    incDate = callbacks[2]
    decDate = callbacks[3]

    dayDisplayFrame = Frame(frame, bg="white")
    dayDisplayFrame.pack(side=LEFT)

    prevDay = Button(dayDisplayFrame, text="<", command=decDate,
                     fg="white", bg="#318c37", activebackground="#40a85c",
                     font=buttonText, width=15)
    dayLabel = Label(dayDisplayFrame, bg="white", text=toDateString(
        currentDate), font=buttonText)
    nextDay = Button(dayDisplayFrame, text=">", command=incDate,
                     fg="white", bg="#318c37", activebackground="#40a85c",
                     font=buttonText, width=15)

    prevDay.grid(column=0, row=0, padx=(50, 10), pady=(10, 10))
    dayLabel.grid(column=1, row=0, padx=(10, 10), pady=(10, 10))
    nextDay.grid(column=2, row=0, padx=(10, 10), pady=(10, 10))

    actionButtonDisplay = Frame(frame, bg="white")
    actionButtonDisplay.pack(side=RIGHT)

    newEvent = Button(actionButtonDisplay, text="New Event", command=openNewEventPopup,
                      fg="white", bg="#318c37", activebackground="#40a85c",
                      font=buttonText, width=15)
    sync = Button(actionButtonDisplay, text="Sync with Calendar", command=syncWithCalendar,
                  fg="white", bg="#318c37", activebackground="#40a85c",
                  font=buttonText, width=15)

    newEvent.grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
    sync.grid(column=1, row=0, padx=(10, 50), pady=(10, 10))


def renderBottomBar(frame, lookAhead, lookBehind):
    buttonText = Font(frame, size=10)
    backwardsButton = Button(frame, text="<", command=lookBehind,
                             fg="white", bg="#318c37", activebackground="#40a85c",
                             font=buttonText, width=2)
    forwardsButton = Button(frame, text=">", command=lookAhead,
                            fg="white", bg="#318c37", activebackground="#40a85c",
                            font=buttonText, width=2)
    moveLabel = Label(frame, text="Shift Hour Range",
                      bg="white", font=buttonText)

    backwardsButton.grid(column=0, row=0, padx=(50, 10), pady=(10, 10))
    forwardsButton.grid(column=1, row=0, padx=(10, 10), pady=(10, 10))
    moveLabel.grid(column=2, row=0, padx=10)
