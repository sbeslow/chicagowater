from datetime import time, datetime


def insert_cso_into_db(c, event):
    sql = "INSERT INTO CSOs (Location, Segment, Date, StartTime, EndTime, Duration) VALUES "

    start = event["start"].strftime("%H:%M")
    stop = event["stop"].strftime("%H:%M")

    sql += "('{loc}',{seg},'{dt}','{st}','{sp}',{dur})".format(loc=event["location"],
                                                                                    seg=event["segment"],
                                                                                    dt=event["date"],
                                                                                    st=start,
                                                                                    sp=stop,
                                                                                    dur=event["duration"])
    c.execute(sql)


def select_from_db(c, sql):

    c.execute(sql)
    rows = c.fetchall()
    if len(rows) == 0:
        return []

    events = []
    for row in rows:
        events.append({"id": row[0], "location": row[1], "segment": row[2], "date": row[3],
                       "start": datetime.strptime(row[4], "%H:%M"),
                       "stop": datetime.strptime(row[5], "%H:%M"), "duration": row[6]})
    return events
