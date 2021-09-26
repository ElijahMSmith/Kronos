from tkinter import *
from Event import *
import util as constants
from tkinter.font import Font

eventViewBg = constants.eventViewBg
eventViewButtonBg = constants.eventViewButtonBg
eventViewButtonBgActive = constants.eventViewButtonBgActive


class NewEventPopupWindow():
    def __init__(self, appendNewEventCallback, currentDate):
        self.rows = 0
        self.currentDate = currentDate
        self.invalidFields = False
        self.entryValues = {}  # .has_key(key_to_lookup):
        self.appendCallback = appendNewEventCallback
        self.createWindow()

    def createWindow(self):
        win = Toplevel()
        win.configure(bg=eventViewBg)
        win.wm_title("New Event/Task")
        self.win = win

        win.bind('<Return>', self.returnPressCallback)

        self.createDataRow("name", "Event Name: ", 50)
        self.createDataRow("description", "Event Description: ", 50)
        self.createDataRow("eventType", "Event Type (Event or Task): ", 50)
        self.createDataRow("start", "Start Time: ", 50)
        self.createDataRow("end", "End Time: ", 50)
        self.createDataRow(
            "actualStart", "Time at Which Item Actually Started (Optional): ", 50)
        self.createDataRow(
            "actualEnd", "Time at Which Item Actually Ended (Optional): ", 50)

        self.actionBarFrame = Frame(self.win, bg=eventViewBg)
        self.rerenderActionBar()

    def createDataRow(self, propertyName, labelText, entryWidth, enabled=True):
        propertyFrame = Frame(self.win, bg=eventViewBg)
        propertyFrame.grid(sticky=W, row=self.rows, column=0, pady=10, padx=10)

        propLabel = Label(propertyFrame, bg=eventViewBg,
                          text=labelText, wraplength=100)
        propLabel.grid(row=0, column=0)

        entryValueText = StringVar()
        propEntry = Entry(propertyFrame, width=entryWidth, textvariable=entryValueText,
                          state=DISABLED if not enabled else NORMAL)
        propEntry.grid(row=0, column=1)

        self.entryValues[propertyName] = entryValueText

        self.rows += 1

    def rerenderActionBar(self):
        barFrame = self.actionBarFrame

        for child in barFrame.winfo_children():
            child.destroy()
        barFrame.grid(sticky=W, row=self.rows, column=0, pady=10)

        buttonText = Font(barFrame, size=12)
        saveButton = Button(barFrame, text="Save Event", command=self.processSaveAttempt,
                            fg="white", bg=eventViewButtonBg, activebackground=eventViewButtonBgActive,
                            font=buttonText)
        saveButton.grid(column=0, row=0, padx=10)

        if self.invalidFields:
            invalidFieldsLabel = Label(
                barFrame, text="Not saved - One or more invalid values provided.", font=buttonText, fg="#fd3535")
            invalidFieldsLabel.grid(column=1, row=0, padx=10)

    def returnPressCallback(self, origin):
        self.processSaveAttempt()

    def processSaveAttempt(self):
        print("Trying to save...")
        try:
            event = Event(self.entryValues["name"].get(), self.entryValues["description"].get(),
                          self.entryValues["start"].get(
            ), self.entryValues["end"].get(),
                actualStart=self.entryValues["actualStart"].get(
            ), actualEnd=self.entryValues["actualEnd"].get(),
                eventType=self.entryValues["eventType"].get(), currentDate=self.currentDate)

            print("Created event successfully")
            self.appendCallback(event)
            print("Appended event successfully")
            self.invalidFields = False
            self.win.destroy()
        except:
            print("Not saved")
            self.invalidFields = True
            self.rerenderActionBar()
