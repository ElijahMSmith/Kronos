from util import getTimeString


class Event:
    def __init__(self, name, description, start="12:00 AM", end="12:01 AM", actualStart=None, actualEnd=None, eventType="event"):
        self.name = name
        self.description = description
        etLower = eventType.lower()
        if not (etLower == "event" or etLower == "task"):
            etLower = "event"
        self.eventType = etLower

        self.start = EventTime(start) if isinstance(start, str) else start
        self.end = EventTime(end) if isinstance(end, str) else end

        if actualStart is None or (isinstance(actualStart, str) and actualStart == ""):
            self.actualStart = self.start
        else:
            self.actualStart = EventTime(
                actualStart) if isinstance(actualStart, str) else actualStart

        if actualEnd is None or (isinstance(actualEnd, str) and actualEnd == ""):
            self.actualEnd = self.end
        else:
            self.actualEnd = EventTime(actualEnd) if isinstance(
                actualEnd, str) else actualEnd

        self.late = self.actualStart > self.start

    def fullyEqual(self, other):
        return self.name == other.name and self.description == other.description and self.start == other.start and self.end == other.end and self.actualStart == other.actualStart and self.actualEnd == other.actualEnd and self.eventType == other.eventType

    def __copy__(self):
        return type(self)(self.name, self.description, self.start, self.end, actualStart=self.actualStart,  actualEnd=self.actualEnd, eventType=self.eventType)

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
        return f"{{name: {self.name}, description: {self.description}, start: {self.start.__str__()}, end: {self.end.__str__()}, realStart: {self.actualStart.__str__()}, readEnd: {self.actualEnd.__str__()}, late: {self.late}, eventType: {self.eventType}}}"

    def __str__(self):
        return f"{{name: {self.name}, description: {self.description}, start: {self.start.__str__()}, end: {self.end.__str__()}, realStart: {self.actualStart.__str__()}, readEnd: {self.actualEnd.__str__()}, late: {self.late}, eventType: {self.eventType}}}"


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
        return getTimeString(self.hour, self.minute)

    def __str__(self):
        return getTimeString(self.hour, self.minute)
