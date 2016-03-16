import datetime

import sqlite3

from mwrd_csos.database_methods import select_from_db


def compare_databases(start_date_str, end_date_str):

    iter_date = datetime.datetime.strptime(start_date_str, "%m/%d/%Y")
    end = datetime.datetime.strptime(end_date_str, "%m/%d/%Y")

    this_sqlite_file = '/Users/scottbeslow/Documents/openGovWorkspace/chicagowater/chicagowater/mwrd_csos/cso-data.db'
    orig_sqlite_file = '/Users/scottbeslow/Documents/openGovWorkspace/chicagowater/chicagowater/mwrd_csos/fromWebOrig.db'

    conn_orig = sqlite3.connect(orig_sqlite_file)
    c_o = conn_orig.cursor()
    conn_this = sqlite3.connect(this_sqlite_file)
    c_n = conn_this.cursor()

    while iter_date <= end:
        date_str = iter_date.strftime("%Y-%m-%d")

        sql = "SELECT * FROM CSOs where Date='%s'" % date_str
        orig_events = select_from_db(c_o, sql)
        this_events = select_from_db(c_n, sql)

        for orig_event in orig_events:
            found = False
            for this_event in this_events:
                if orig_event.equals(this_event):
                    found = True
                    break
            if found is False:
                print "Failed on event %s" % orig_event.to_string()
                conn_orig.close()
                conn_this.close()
                return

        iter_date += datetime.timedelta(days=1)

    conn_orig.close()
    conn_this.close()

compare_databases("1/7/2007", "1/1/2012")