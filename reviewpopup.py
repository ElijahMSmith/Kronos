from tkinter import *
from Event import *
import util as constants
from tkinter.font import Font

breakdownBg = constants.breakdownBg
dangerCategoryFg = "#850000"
goodCategoryFg = "#008516"


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

            ms = (event.end - event.actualEnd).total_seconds() / 60
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

        self.statsFrame = Frame(win, bg=breakdownBg)
        self.statsFrame.pack(side=LEFT)

        self.genLabel(
            "Total Minutes Allocated to Engagements (Concurrent)", stats[0], category="NEUTRAL")
        self.genLabel("Total Minutes Spent on Events",
                      stats[1], category="NEUTRAL")
        self.genLabel("Total Minutes Spent on Tasks",
                      stats[2], category="NEUTRAL")
        self.genLabel("Total Minutes Not in Engagements",
                      str(round(stats[3], 2)) + "/" + str(24 * 60), category="GOOD")
        self.genLabel("Percentage of Day Not in Engagements",
                      stats[4], True, category="GOOD")

        self.genLabel("Number of Engagements Started on Time",
                      stats[5], category="GOOD")
        self.genLabel("Number of Engagements Started Late",
                      stats[6], category="DANGER")
        self.genLabel("Number of Engagements Finished Early",
                      stats[7], category="GOOD")

        self.genLabel(
            "Percentage of Engagements Started on Time", stats[8], True, category="GOOD")
        self.genLabel("Percentage of Engagements Started Late",
                      stats[9], True, category="DANGER")
        self.genLabel("Percentage of Engagements Finished Early",
                      stats[10], True, category="GOOD")

        self.genLabel("Minutes Saved from Engagements",
                      stats[11], category="GOOD")

        self.genLabel("Number of Total Late Minutes",
                      stats[12], category="DANGER")
        self.genLabel("Percentage Late of Total Minutes",
                      stats[13], True, category="DANGER")
        self.genLabel("Most Late Started Engagement",
                      stats[14], category="DANGER")
        self.genLabel("Most Late Minutes of Any Engagement",
                      stats[15], category="DANGER")

        barFrame = Frame(win, bg=breakdownBg)
        barFrame.pack(side=RIGHT)
        frameLabel = Label(barFrame, text='Minutes Per Category',
                           font=self.labelFont)
        frameLabel.grid(row=0, column=0)

        data = [stats[1], stats[2], stats[3], stats[11], stats[12]]
        colors = ["#31a33a",  "#cf7800", "#bf3000", "#0076bf", "#4300bf"]

        maxHeight = max(data) * 1.1

        c_width = 400
        c_height = 400
        gapWidth = 40
        barWidth = (400 - (gapWidth * (len(data) + 1))) / len(data)
        c = Canvas(barFrame, width=c_width, height=c_height)
        c.grid(row=1, column=0)

        for i in range(0, len(data)):
            barHeight = data[i]/maxHeight * (c_height - 40)
            x0 = gapWidth * (i + 1) + barWidth * (i)
            x1 = x0 + barWidth
            y0 = c_height - 20
            y1 = c_height - 20 - barHeight

            # Here we draw the bar
            c.create_rectangle(x0, y0, x1, y1, fill=colors[i])
            c.create_text(x0 + 15, y0 + 10, text=str(data[i]))

        keyLabel1 = Label(barFrame, text='# Minutes of Events',
                          font=self.labelFont, fg=colors[0], bg=breakdownBg)
        keyLabel1.grid(row=2, column=0)

        keyLabel2 = Label(barFrame, text='# Minutes of Tasks',
                          font=self.labelFont, fg=colors[1], bg=breakdownBg)
        keyLabel2.grid(row=3, column=0)

        keyLabel3 = Label(barFrame, text='# Minutes not in Engagements',
                          font=self.labelFont, fg=colors[2], bg=breakdownBg)
        keyLabel3.grid(row=4, column=0)

        keyLabel4 = Label(barFrame, text='# Minutes Saved',
                          font=self.labelFont, fg=colors[3], bg=breakdownBg)
        keyLabel4.grid(row=5, column=0)

        keyLabel5 = Label(barFrame, text='# Late Minutes',
                          font=self.labelFont, fg=colors[4], bg=breakdownBg)
        keyLabel5.grid(row=6, column=0)

    def genLabel(self, text, value, percent=False, category="NEUTRAL"):
        adjustedValue = value
        if not isinstance(value, str):
            adjustedValue = str(
                round(value if (not percent) else (value * 100), 2))

        innerFrame = Frame(self.statsFrame, bg=breakdownBg)
        innerFrame.grid(row=self.row, padx=10, pady=10)
        labelPrefix = Label(innerFrame, text=text + ": ",
                            font=self.labelFont, bg=breakdownBg)
        labelPrefix.grid(row=0, column=0)
        labelSuffix = Label(innerFrame, text=adjustedValue + ("%" if percent else ""),
                            font=self.labelFont, bg=breakdownBg, fg=(dangerCategoryFg if category == "DANGER" else (goodCategoryFg if category == "GOOD" else "black")))
        labelSuffix.grid(row=0, column=1)
        self.row += 1

    def destroyWindow(self, eventOrigin):
        self.win.destroy()
