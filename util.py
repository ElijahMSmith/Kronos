import datetime


def toDateString(dt):
    return dt.strftime("%m/%d/%Y")


def getTimeString(datetime):
    hour = datetime.hour
    minute = datetime.minute

    if hour < 12:
        if hour == 0:
            hour == 12
        return str(hour) + ":" + ("0" if minute < 10 else "") + str(minute) + " AM"
    else:
        if hour != 12:
            hour %= 12
        return str(hour) + ":" + ("0" if minute < 10 else "") + str(minute) + " PM"


def getDateTime(currentDateTime, timeString):
    pieces = timeString.split(":")
    hourVal = int(pieces[0])
    minuteVal = int(pieces[1][0:2])
    suffixString = (pieces[1][len(pieces[1])-2:])
    PM = suffixString.lower() == "pm"

    if PM == True:
        if hourVal != 12:
            hourVal = hourVal + 12
        else:
            hourVal = 12
    else:
        if hourVal != 12:
            hourVal = hourVal
        else:
            hourVal = 0

    return currentDateTime.replace(
        hour=hourVal, minute=minuteVal, second=0, microsecond=0)


canvWidth = 1400
canvHeight = 850
cellWidth = 200
eventBg = "#3065ba"
taskBg = "#2aa36f"
lateBg = "#b02c42"
eventViewBg = "#fafaa5"
eventViewButtonBg = "#002cbd"
eventViewButtonBgActive = "#003afa"
breakdownBg = "#ffbf91"
