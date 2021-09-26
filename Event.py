from util import getDateTime
import shortuuid
import datetime


class Event:
    def __init__(self, name, description, start="12:00 AM", end="12:01 AM", actualStart=None, actualEnd=None, eventType="event", existingUUID=None, fromGoogle=False, currentDate=datetime.datetime.now()):
        self.name = name
        self.description = description
        self.currentDate = currentDate
        etLower = eventType.lower()
        if not (etLower == "event" or etLower == "task"):
            etLower = "event"
        self.eventType = etLower

        self.fromGoogle = fromGoogle

        if existingUUID is None:
            self.uuid = shortuuid.uuid()
        else:
            self.uuid = existingUUID

        self.start = getDateTime(currentDate, start) if isinstance(
            start, str) else start
        self.end = getDateTime(
            currentDate, end) if isinstance(end, str) else end

        if actualStart is None or (isinstance(actualStart, str) and actualStart == ""):
            self.actualStart = self.start
        else:
            self.actualStart = getDateTime(currentDate,
                                           actualStart) if isinstance(actualStart, str) else actualStart

        if actualEnd is None or (isinstance(actualEnd, str) and actualEnd == ""):
            self.actualEnd = self.end
        else:
            self.actualEnd = getDateTime(currentDate, actualEnd) if isinstance(
                actualEnd, str) else actualEnd

        self.late = self.actualStart > self.start

    def __copy__(self):
        return type(self)(self.name, self.description, self.start, self.end, actualStart=self.actualStart, actualEnd=self.actualEnd, eventType=self.eventType, existingUUID=self.uuid, fromGoogle=self.fromGoogle, currentDate=self.currentDate)

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
        return f"{{name: {self.name}, description: {self.description}, uuid: {self.uuid.__str__()}, start: {self.start.__str__()}, end: {self.end.__str__()}, realStart: {self.actualStart.__str__()}, readEnd: {self.actualEnd.__str__()}, late: {self.late}, eventType: {self.eventType}, fromGoogle: {self.fromGoogle}}}"

    def __str__(self):
        return f"{{name: {self.name}, description: {self.description}, uuid: {self.uuid.__str__()}, start: {self.start.__str__()}, end: {self.end.__str__()}, realStart: {self.actualStart.__str__()}, readEnd: {self.actualEnd.__str__()}, late: {self.late}, eventType: {self.eventType}, fromGoogle: {self.fromGoogle}}}"
