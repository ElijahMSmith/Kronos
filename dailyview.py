from tkinter import *
from Event import *
from util import constants
from tkinter.font import Font

startHour = 0
startMinute = 0

canvWidth = constants["canvWidth"]
canvHeight = constants["canvHeight"]
cellWidth = constants["cellWidth"]
cellYOffset = 50

rowEvents = [[]]


# Used to write text inside each cell and not expand beyond

def make_label(master, x, y, h, w, fs, *args, **kwargs):
    buttonText = Font(frame, size=fs)
    f = Frame(master, height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)
    label = Label(f, *args, **kwargs)
    label.pack(fill=BOTH, expand=1)
    return label


def renderCalendar(outerFrame, scheduledData, canvStartHour):
    canvas = Canvas(outerFrame, bg="white", height=canvHeight, width=canvWidth,
                    bd=5)
    canvas.pack()
    renderEvents(canvas, scheduledData, canvStartHour)


'''
Get click position, which may or may not be on top of an event
def key(event):
    print "pressed", repr(event.char)

def callback(event):
    print "clicked at", event.x, event.y

canvas= Canvas(root, width=100, height=100)
canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback)
canvas.pack()
'''


def renderEvents(canvas, scheduledData, canvStartHour):
    timeLabels = Font(canvas, size=10)
    rowEvents = [[]]

    # somewidget.winfo_width()

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

            # print(event)

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

            canvas.create_rectangle(
                attr[0], attr[1], attr[2], attr[3], fill="red")
