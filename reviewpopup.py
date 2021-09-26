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
        finishedEarly = 0

        totalMinutes = 0
        lateMinutes = 0
        eventMinutes = 0
        taskMinutes = 0
        minutesSaved = 0

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

            if event.actualEnd < event.end:
                finishedEarly += 1

            ms = (event.actualEnd - event.end).total_seconds() / 60
            if ms < 0:
                ms = 0
            minutesSaved += ms

        # Algorithm: Get the percentage of time the person was not in an engagement during the day
        # NOTE: I'm using actualStart and actualEnd to reflect the actual course of the day
        usedMinutes = 0
        indices = []
        l = len(scheduledData)
        while len(indices) < l:
            indices.append(0)

        startRow = -1
        start = None
        end = None

        while True:

            start = None
            startRow = -1
            # 1. Find the start time from the min of all rows at their current indices
            for i in range(0, l):
                # If this row doesn't have any more events than we skip it
                if len(scheduledData[i]) <= indices[i]:
                    continue

                thisStart = scheduledData[i][indices[i]].actualStart

                if start is None or thisStart < start:
                    start = thisStart
                    startRow = i

            # 1.5. If we don't have any more events in the list, we're done
            if start is None:
                break

            # 2. Set end to be the end of this earliest event
            end = scheduledData[startRow][indices[startRow]].actualEnd
            indices[startRow] += 1  # Next event

            # 3. While there are more events in any row that start before/at end and extend past,
            #    update end to be the end of that event, increment that row
            while True:
                goAgain = False
                for j in range(0, l):
                    # If this row doesn't have any more events than we skip it
                    if len(scheduledData[j]) <= indices[j]:
                        continue

                    thisEvent = scheduledData[j][indices[j]]

                    # If there is a gap between end and this event, skip for now
                    if thisEvent.actualStart > end:
                        continue

                    # This event has already been passed, ignore it and move to next event
                    if thisEvent.actualEnd < end:
                        indices[j] += 1
                        continue

                    if thisEvent.actualStart <= end and thisEvent.actualEnd > end:
                        end = thisEvent.actualEnd
                        indices[j] += 1
                        goAgain = True
                if not goAgain:
                    break

            # 4. Add all the minutes between start/end, which contain at least one event, to usedMinutes
            usedMinutes += (end - start).total_seconds() / 60

            print(str((end - start).total_seconds() / 60) +
                  " minutes between " + str(start) + " to " + str(end))

            # 5. Move all indices to the next event where event.actualStart >= end (from this iteration)
            for k in range(0, l):
                # While there is another event in this row and it starts too early, skip it
                while len(scheduledData[k]) > indices[k] and scheduledData[k][indices[k]].actualStart < end:
                    indices[k] += 1

            # 6. Repeat

        percentFree = 1 - (usedMinutes / (24 * 60.0))

        return (totalMinutes, eventMinutes, taskMinutes, 24 * 60 - usedMinutes, percentFree, totalActivities - lateActivities, lateActivities, finishedEarly, 1.0*(totalActivities - lateActivities)/totalActivities, 1.0*lateActivities/totalActivities, 1.0*finishedEarly/totalActivities, minutesSaved, lateMinutes, 1.0 * lateMinutes / totalMinutes, mostLateEvent, mostLateEventMinutes)

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
        self.genLabel("Total Minutes Not in Engagements",
                      str(round(stats[3], 2)) + "/" + str(24 * 60))
        self.genLabel("Percentage of Time Not in Engagements", stats[4], True)

        self.genLabel("Number of Engagements Started on Time", stats[5])
        self.genLabel("Number of Engagements Started Late", stats[6])
        self.genLabel("Number of Engagements Finished Early", stats[7])

        self.genLabel(
            "Percentage of Engagements Started on Time", stats[8], True)
        self.genLabel("Percentage of Engagements Started Late", stats[9], True)
        self.genLabel("Percentage of Engagements Finished Early",
                      stats[10], True)

        self.genLabel("Minutes Saved from Engagements", stats[11])

        self.genLabel("Number of Total Late Minutes", stats[12])
        self.genLabel("Percentage Late of Total Minutes", stats[13], True)
        self.genLabel("Most Late Started Engagement", stats[14])
        self.genLabel("Most Late Minutes of Any Engagement", stats[15])

    def genLabel(self, text, value, percent=False):
        adjustedValue = value
        if not isinstance(value, str):
            adjustedValue = str(
                round(value if (not percent) else (value * 100), 2))

        label = Label(self.win, text=text + ": " + adjustedValue + ("%" if percent else ""),
                      font=self.labelFont, bg=breakdownBg)
        label.grid(row=self.row, column=0, padx=10, pady=10)
        self.row += 1

    def destroyWindow(self, eventOrigin):
        self.win.destroy()
