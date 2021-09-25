class Event:
    def __init__(self, name, description, start, end):
        self.name = name
        self.description = description
        self.start = EventTime(start)
        self.end = EventTime(end)
        self.actualStart = EventTime(start)
        self.actualEnd = EventTime(end)
        self.late = False

    def __lt__(self, other):
        return self.start.__lt__(other.start)

    def __le__(self, other):
        return self.start.__le__(other.start)

    def __eq__(self, other):
        return self.start.__eq__(other.start)

    def __ne__(self, other):
        return self.start.__ne__(other.start)

    def __gt__(self, other):
        return self.start.__gt__(other.start)

    def __ge__(self, other):
        return self.start.__ge__(other.start)

    def __repr__(self):
        return f"{{name: {self.name}, description: {self.description}, start: {self.start.__str__()}, end: {self.end.__str__()}, realStart: {self.actualStart.__str__()}, readEnd: {self.actualEnd.__str__()}, late: {self.late}}}"

    def __str__(self):
        return f"{{name: {self.name}, description: {self.description}, start: {self.start.__str__()}, end: {self.end.__str__()}, realStart: {self.actualStart.__str__()}, readEnd: {self.actualEnd.__str__()}, late: {self.late}}}"


class EventTime:
    def __init__(self, timeString):
        self.timeString = timeString

        pieces = timeString.split(":")
        hour = int(pieces[0])
        minute = int(pieces[1][0:2])
        suffixString = (pieces[1][len(pieces[1])-2:])
        PM = suffixString.lower() == "pm"

        if PM == True:
            if hour != 12:
                self.hour = hour + 12
            else:
                self.hour = 12
        else:
            if hour != 12:
                self.hour = hour
            else:
                self.hour = 0

        self.minute = minute

    def __lt__(self, other):
        return self.hour < other.hour or (self.hour == other.hour and self.minute < other.minute)

    def __le__(self, other):
        return self.hour < other.hour or (self.hour == other.hour and self.minute <= other.minute)

    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute

    def __ne__(self, other):
        return not (self.hour == other.hour and self.minute == other.minute)

    def __gt__(self, other):
        return self.hour > other.hour or (self.hour == other.hour and self.minute > other.minute)

    def __ge__(self, other):
        return self.hour > other.hour or (self.hour == other.hour and self.minute >= other.minute)

    def __repr__(self):
        return f"{{H:{self.hour}, M:{self.minute}}}"

    def __str__(self):
        return f"{{H:{self.hour}, M:{self.minute}}}"
