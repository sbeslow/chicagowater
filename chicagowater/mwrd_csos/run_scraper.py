from datetime import datetime

from scraper import scrape_date
import sqlite3
import time

sqlite_file = 'cso-data.db'
events = scrape_date("9/18/2015")

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

for event in events:

    event["StartTime"] = event["StartTime"].strftime('%H:%M')

    event["EndTime"] = event["EndTime"].strftime('%H:%M')

    try:
        c.execute("INSERT INTO CSOs (Location, Segment, Date, StartTime, EndTime, Duration) VALUES " +
                  "('{loc}',{seg},'{dt}','{st}','{et}',{dur})".format(loc=event["Location"], seg=event["Segment"],
                    dt=event["Date"], st=event["StartTime"], et=event["EndTime"], dur=event["Duration"]))

    except Exception as e:
        print('Exception: %s' % e.message)

conn.commit()
conn.close()
