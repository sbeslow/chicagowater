class CsoEvent(object):
    def __init__(self, location, segment, date_str, start, stop, duration, event_id=None):
        self.location = location
        self.segment = segment
        self.date_str = date_str
        self.start = start
        self.stop = stop
        self.duration = duration
        self.event_id = event_id

    def insert_sql(self):
        sql = "INSERT INTO CSOs (Location, Segment, Date, StartTime, EndTime, Duration) VALUES "

        sql += "('{loc}',{seg},'{dt}','{st}','{sp}',{dur})".format(loc=self.location,
                                                                   seg=self.segment,
                                                                   dt=self.date_str,
                                                                   st=self.start.strftime("%H:%M"),
                                                                   sp=self.stop.strftime("%H:%M"),
                                                                   dur=self.duration)
        return sql

    def to_string(self):
        return "ID: %s  Location: %s  Segment:  %s  Date: %s  Start:  %s  Stop: %s  Duration %s" % (
            self.event_id, self.location, self.segment, self.date_str, self.start, self.stop, self.duration)
