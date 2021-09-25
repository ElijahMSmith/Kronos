def getTimeString(hour, minute):
    if hour < 12:
        if hour == 0:
            hour == 12
        return str(hour) + ":" + ("0" if minute < 10 else "") + str(minute) + " AM"
    else:
        if hour != 12:
            hour %= 12
        return str(hour) + ":" + ("0" if minute < 10 else "") + str(minute) + " PM"


canvWidth = 1400
canvHeight = 850
cellWidth = 200
eventBg = "#3065ba"
taskBg = "#2aa36f"
lateBg = "#b02c42"
eventViewBg = "#fafaa5"
eventViewButtonBg = "#002cbd"
eventViewButtonBgActive = "#003afa"
