from tkinter import *
from Event import *
import util as constants
from tkinter.font import Font

breakdownBg = constants.breakdownBg


class ReviewPopup():
    def __init__(self, currentDate, eventData, scheduledData, frequency="Daily"):
        # frequency = "Daily" || "Weekly"
        self.stats = self.calculateDailyStatistics(
            eventData, scheduledData, frequency)
        self.currentDate = currentDate
        self.frequency = frequency
        self.createWindow()

    def calculateDailyStatistics(self, eventData, scheduledData, frequency):
        # Note: Minutes for each event are counted separately even if are the same instance of time
        # The only metric that does something different is the % day free value
        totalActivities = len(eventData)
        lateActivities = 0

        totalMinutes = 0
        lateMinutes = 0
        eventMinutes = 0
        taskMinutes = 0

        mostLateEventMinutes = 0
        mostLateEvent = "N/A"  # event.name

        for event in eventData:
            #(datetime1 - datetime2).total_seconds() / 60
            elapsedTime = event.end - event.start
            eMinutes = elapsedTime.total_seconds() / 60

            elapsedLateTime = event.actualStart - event.start
            eLateMinutes = elapsedLateTime.total_seconds() / 60
            if eLateMinutes < 0:
                eLateMinutes = 0

            lateActivities += 1 if event.late else 0
            totalMinutes += eMinutes
            lateMinutes += eLateMinutes

            if event.eventType == "task":
                taskMinutes += eMinutes
            else:
                eventMinutes += eMinutes

            if eLateMinutes >= mostLateEventMinutes:
                mostLateEventMinutes = eLateMinutes
                mostLateEvent = event.name

        # Get the percentage of time the person was not in an engagement during the day
        freeMinutes = 0
        startTime = 0
        endTime = 0

        return (totalMinutes, eventMinutes, taskMinutes, percentFree, totalActivities - lateActivities, lateActivities, 1.0*(totalActivities - lateActivities)/totalActivities, 1.0*lateActivities/totalActivities, lateMinutes, 1.0 * lateMinutes / totalMinutes, mostLateEvent, mostLateEventMinutes)

    def createWindow(self):
        win = Toplevel()
        win.configure(bg=breakdownBg)
        win.wm_title(self.frequency.capitalize() + "Breakdown")
        win.bind('<Return>', self.destroyWindow)
        self.win = win

        self.row = 0

        stats = self.stats
        self.labelFont = Font(win, size=12)

        self.genLabel("Total Minutes Spent in Engagements", stats[0])
        self.genLabel("Total Minutes Spent on Events", stats[1])
        self.genLabel("Total Minutes Spent on Tasks", stats[2])
        self.genLabel("Percentage of Time Not in Engagements", stats[3])
        self.genLabel("Number of Engagements Started on Time", stats[4])
        self.genLabel("Number of Engagements Started Late", stats[5])
        self.genLabel(
            "Percentage of Engagements Started on Time", stats[6], True)
        self.genLabel("Percentage of Engagements Started Late", stats[7], True)
        self.genLabel("Number of Total Late Minutes", stats[8])
        self.genLabel("Percentage Late of Total Minutes", stats[9], True)
        self.genLabel("Most Late Started Engagement", stats[10])
        self.genLabel("Most Late Minutes of Any Engagement", stats[11])

    def genLabel(self, text, value, percent=False):
        label = Label(self.win, text=text + ": " + str(round(value if not percent else value * 100, 2)) + ("%" if percent else ""),
                      font=self.labelFont, bg=breakdownBg)
        label.grid(row=self.row, column=0, padx=10, pady=10)
        self.row += 1

    def destroyWindow(self, eventOrigin):
        self.win.destroy()
