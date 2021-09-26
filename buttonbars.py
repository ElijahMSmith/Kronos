from tkinter import *
from tkinter.font import Font
from Event import *
from neweventview import *
from util import toDateString
import datetime

addNewEventCallback = None
popup = None


def openNewEventPopup(currentDate):
    global popup
    if not(popup is None) and not (popup.win is None):
        popup.win.destroy()
    popup = NewEventPopupWindow(addNewEventCallback, currentDate)


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

    newEvent = Button(actionButtonDisplay, text="New Event", command=lambda: openNewEventPopup(currentDate),
                      fg="white", bg="#318c37", activebackground="#40a85c",
                      font=buttonText, width=15)
    sync = Button(actionButtonDisplay, text="Sync with Calendar", command=syncWithCalendar,
                  fg="white", bg="#318c37", activebackground="#40a85c",
                  font=buttonText, width=15)

    newEvent.grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
    sync.grid(column=1, row=0, padx=(10, 50), pady=(10, 10))


def renderBottomBar(frame, callbacks):
    lookAhead = callbacks[0]
    lookBehind = callbacks[1]
    dailyReview = callbacks[2]
    weeklyReview = callbacks[3]
    buttonText = Font(frame, size=10)

    pageManipulation = Frame(frame, bg="white")
    pageManipulation.pack(side=LEFT)

    backwardsButton = Button(pageManipulation, text="<", command=lookBehind,
                             fg="white", bg="#318c37", activebackground="#40a85c",
                             font=buttonText, width=2)
    moveLabel = Label(pageManipulation, text="Shift Hour Range",
                      bg="white", font=buttonText)
    forwardsButton = Button(pageManipulation, text=">", command=lookAhead,
                            fg="white", bg="#318c37", activebackground="#40a85c",
                            font=buttonText, width=2)

    backwardsButton.grid(column=0, row=0, padx=(50, 10), pady=(10, 10))
    moveLabel.grid(column=1, row=0, padx=10)
    forwardsButton.grid(column=2, row=0, padx=(10, 10), pady=(10, 10))

    reviewFrame = Frame(frame, bg="white")
    reviewFrame.pack(side=RIGHT)

    dailyReviewButton = Button(reviewFrame, text="Daily Review", command=dailyReview,
                               fg="white", bg="#318c37", activebackground="#40a85c",
                               font=buttonText)
    weeklyReviewButton = Button(reviewFrame, text="Weekly Review", command=weeklyReview,
                                fg="white", bg="#318c37", activebackground="#40a85c",
                                font=buttonText)

    dailyReviewButton.grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
    weeklyReviewButton.grid(column=1, row=0, padx=(10, 50), pady=(10, 10))
