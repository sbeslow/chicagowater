from datetime import datetime

from mwrd_csos.events import CsoEvent


def insert_cso_into_db(c, event):
    sql = event.insert_sql()

    c.execute(sql)


def select_from_db(c, sql):
    c.execute(sql)
    rows = c.fetchall()
    if len(rows) == 0:
        return []

    events = []
    for row in rows:
        events.append(
            CsoEvent(row[1], row[2], row[3], datetime.strptime(row[4], "%H:%M"), datetime.strptime(row[5], "%H:%M"),
                     row[6], row[0]))

    return events


def delete_from_db(c, event):
    if event.event_id is None:
        raise Exception("Event does not have an id")

    sql = "DELETE FROM CSOs WHERE ID=" + event.event_id
    c.execute(sql)
