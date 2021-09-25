from tkinter import *
from tkinter.font import Font


def renderTopBar(frame, createNewEvent, syncWithCalendar):
    buttonText = Font(frame, size=20)
    newEvent = Button(frame, text="New Event", command=createNewEvent,
                      fg="white", bg="#318c37", activebackground="#40a85c",
                      font=buttonText, width=15)
    sync = Button(frame, text="Sync with Calendar", command=syncWithCalendar,
                  fg="white", bg="#318c37", activebackground="#40a85c",
                  font=buttonText, width=15)

    newEvent.grid(column=1, row=0, padx=(10, 10), pady=(10, 10))
    sync.grid(column=2, row=0, padx=(10, 10), pady=(10, 10))


def renderBottomBar(frame, lookAhead, lookBehind):
    buttonText = Font(frame, size=10)
    backwardsButton = Button(frame, text="<", command=lookBehind,
                             fg="white", bg="#318c37", activebackground="#40a85c",
                             font=buttonText, width=2)
    forwardsButton = Button(frame, text=">", command=lookAhead,
                            fg="white", bg="#318c37", activebackground="#40a85c",
                            font=buttonText, width=2)

    backwardsButton.grid(column=1, row=0, padx=(50, 10), pady=(10, 10))
    forwardsButton.grid(column=2, row=0, padx=(10, 10), pady=(10, 10))
