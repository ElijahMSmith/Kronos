from tkinter import *
from Event import *
import util as constants
from tkinter.font import Font
from eventview import *

startHour = 0
startMinute = 0

canvWidth = constants.canvWidth
canvHeight = constants.canvHeight
cellWidth = constants.cellWidth
eventBg = constants.eventBg
taskBg = constants.taskBg
lateBg = constants.lateBg
cellYOffset = 50

rowEvents = [[]]

canvasFrame = None
canvas = None

updateEventCallback = None
deleteEventCallback = None

popup = None


def createEventPopup(forEvent):
    global popup
    if not(popup is None) and not (popup.win is None):
        popup.win.destroy()
    popup = PopupWindow(forEvent, updateEventCallback, deleteEventCallback)


# Get click position and determine which event is being clicked on
def clickCallback(clickOrigin):
    clickx = clickOrigin.x
    clicky = clickOrigin.y
    for row in rowEvents:
        for renderAttr in row:
            x0 = renderAttr[0]
            y0 = renderAttr[1]
            x1 = renderAttr[2]
            y1 = renderAttr[3]
            event = renderAttr[4]

            if clickx >= x0 and clickx <= x1 and clicky >= y0 and clicky <= y1:
                createEventPopup(event)
                return


# Change cursor when it's over an event
def mouseMoved(mouseOrigin):
    mousex = mouseOrigin.x
    mousey = mouseOrigin.y
    for row in rowEvents:
        for renderAttr in row:
            x0 = renderAttr[0]
            y0 = renderAttr[1]
            x1 = renderAttr[2]
            y1 = renderAttr[3]
            event = renderAttr[4]

            # checks whether the mouse is inside the boundrys
            if x0 <= mousex and x1 >= mousex and y0 <= mousey and y1 >= mousey:
                canvas.config(cursor="hand1")
                return

    canvas.config(cursor="")


def renderCalendar(outerFrame, scheduledData, canvStartHour, callbacks):
    global canvasFrame, canvas, updateEventCallback, deleteEventCallback
    canvasFrame = outerFrame
    updateEventCallback = callbacks[0]
    deleteEventCallback = callbacks[1]

    canvas = Canvas(outerFrame, bg="white", height=canvHeight, width=canvWidth,
                    bd=5)
    canvas.bind("<Button-1>", clickCallback)
    canvas.bind("<Motion>", mouseMoved)
    canvas.pack()
    renderEvents(canvas, scheduledData, canvStartHour)
    print("Finished canvas render")


def renderEvents(canvas, scheduledData, canvStartHour):
    global rowEvents
    eventLabelFS = 15
    timeLabels = Font(canvas, size=10)
    eventLabels = Font(canvas, size=eventLabelFS)
    eventLabelCharWidth = eventLabels.measure("m")

    rowEvents = [[]]

    # Draw lines to mark specific hours, based on what the current range is
    # Also put labels for the hours at the top
    for i in range(0, canvWidth, cellWidth):
        line = canvas.create_line(
            i, cellYOffset, i, canvHeight, width=1)

        if i == 0:
            continue

        displayHour = canvStartHour+(i/cellWidth)
        if displayHour == 0:
            displayHour = 12
        elif displayHour > 12:
            displayHour = displayHour % 12

        text = canvas.create_text(i, 30, fill="darkblue", text=str(
            int(displayHour))+":00"+("PM" if canvStartHour >= 12 else "AM"), font=timeLabels)

    # Render events as blocks under the correct time
    # The correct index has already been determined by the function in main, so we put it
    # on the line corresponding to its index in the 2D list
    for index in range(0, len(scheduledData)):
        for event in scheduledData[index]:
            start = event.start
            end = event.end

            # If the event isn't on the calendar, don't bother rendering it
            if end.hour + end.minute/60.0 < canvStartHour or start.hour + start.minute/60.0 > canvStartHour + canvWidth/cellWidth:
                continue

            ix = start.hour - canvStartHour

            x0 = ix * cellWidth + start.minute/60 * cellWidth
            diff = ((end.hour + end.minute/60.0) -
                    (start.hour + start.minute/60.0))
            x1 = x0 + cellWidth * diff
            y0 = cellYOffset + index * cellWidth
            y1 = cellYOffset + (index + 1) * cellWidth

            attr = (x0, y0, x1, y1, event)

            while len(rowEvents) <= index:
                rowEvents.append([])
            rowEvents[index].append(attr)

            fillColor = eventBg
            if event.eventType == "task":
                fillColor = taskBg

            if event.late:
                fillColor = lateBg

            canvas.create_rectangle(
                attr[0], attr[1], attr[2], attr[3], fill=fillColor)

            # Create each line on the event individually until we can't safely create a new line of text
            i = 0
            lineNum = 0
            lineWidth = x1 - x0
            charsPerLine = int(lineWidth/eventLabelCharWidth)

            while i < len(event.name):
                lineText = event.name[i:i + charsPerLine].strip()
                xStart = x0 + 20
                yStart = y0 + 20 + eventLabelFS * lineNum + 5 * lineNum

                # If we've reached the last possible line, don't render any more text
                if yStart + eventLabelFS > y1 - 20:
                    break

                canvas.create_text(xStart,
                                   yStart, fill="white",
                                   text=lineText,
                                   font=eventLabels, anchor=NW),
                i += charsPerLine
                lineNum += 1
