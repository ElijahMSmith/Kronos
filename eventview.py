from tkinter import *
from Event import *
import util as constants
from tkinter.font import Font

eventViewBg = constants.eventViewBg
eventViewButtonBg = constants.eventViewButtonBg
eventViewButtonBgActive = constants.eventViewButtonBgActive


class PopupWindow():
    def __init__(self, event, updateEventCallback, deleteEventCallback):
        self.previousEvent = event.__copy__()
        self.event = event
        self.invalidFields = False
        self.updateEventCallback = updateEventCallback
        self.deleteEventCallback = deleteEventCallback
        self.rows = 0
        self.entryValues = {}
        self.createWindow()

    # Needs to have a display for each element of the event
    # Can change each value and click a save button to update on the canvas
    # Also needs a delete button to remove from everything
    def createWindow(self):
        # event has name, description, type, start, end, actualStart, actualEnd, and late
        event = self.event

        win = Toplevel()
        win.configure(bg=eventViewBg)
        win.wm_title("Viewing: " + event.name)
        self.win = win

        self.createDataRow("name", "Event Name: ", 50)
        self.createDataRow("description", "Event Description: ", 50)
        self.createDataRow("eventType", "Event Type (Event or Task): ", 50)
        self.createDataRow("start", "Start Time: ", 50)
        self.createDataRow("end", "End Time: ", 50)
        self.createDataRow(
            "actualStart", "Time at Which Item Actually Started: ", 50)
        self.createDataRow(
            "actualEnd", "Time at Which Item Actually Ended: ", 50)

        self.actionBarFrame = Frame(self.win, bg=eventViewBg)
        self.renderActionBar()

    def createDataRow(self, propertyName, labelText, entryWidth, enabled=True):
        propertyFrame = Frame(self.win, bg=eventViewBg)
        propertyFrame.grid(sticky=W, row=self.rows, column=0, pady=10, padx=10)

        propLabel = Label(propertyFrame, bg=eventViewBg,
                          text=labelText, wraplength=100)
        propLabel.grid(row=0, column=0)

        entryValueText = StringVar()
        entryValueText.set(str(getattr(self.previousEvent, propertyName)))
        propEntry = Entry(propertyFrame, width=entryWidth, textvariable=entryValueText,
                          state=DISABLED if not enabled else NORMAL)
        propEntry.grid(row=0, column=1)

        self.entryValues[propertyName] = entryValueText

        self.rows += 1

    def renderActionBar(self):
        barFrame = self.actionBarFrame

        for child in barFrame.winfo_children():
            child.destroy()
        barFrame.grid(sticky=W, row=self.rows, column=0, pady=10)

        buttonText = Font(barFrame, size=12)
        backwardsButton = Button(barFrame, text="Save Changes", command=self.processUpdate,
                                 fg="white", bg=eventViewButtonBg, activebackground=eventViewButtonBgActive,
                                 font=buttonText)
        forwardsButton = Button(barFrame, text="Delete Event", command=self.processDeletion,
                                fg="white", bg=eventViewButtonBg, activebackground=eventViewButtonBgActive,
                                font=buttonText)

        backwardsButton.grid(column=0, row=0, padx=10)
        forwardsButton.grid(column=1, row=0, padx=10)

        if self.invalidFields:
            invalidFieldsLabel = Label(
                barFrame, text="Not saved - One or more invalid values provided.", font=buttonText, fg="#fd3535")
            invalidFieldsLabel.grid(column=2, row=0, padx=10)

    def processUpdate(self):
        try:
            self.event = Event(self.entryValues["name"].get(), self.entryValues["description"].get(),
                               self.entryValues["start"].get(
            ), self.entryValues["end"].get(),
                actualStart=self.entryValues["actualStart"].get(
            ), actualEnd=self.entryValues["actualEnd"].get(),
                eventType=self.entryValues["eventType"].get())

            retVal = self.updateEventCallback(self.previousEvent, self.event)
            if retVal:
                self.previousEvent = self.event
        except:
            print("Failed to update: One or more invalid values provided")
            self.invalidFields = True
            self.renderActionBar()

    def processDeletion(self):
        retVal = self.deleteEventCallback(self.previousEvent)
        if retVal:
            self.win.destroy()
