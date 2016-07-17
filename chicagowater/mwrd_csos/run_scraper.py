import datetime
import logging
import sqlite3

from database_methods import insert_cso_into_db

from database_methods import delete_from_db

from helpers import find_overlapping_times
from scraper import scrape_date

sqlite_file = 'cso-data.db'
timestamp_now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
logging.basicConfig(filename='mwrd_scrape_%s.log' % timestamp_now, level=logging.INFO)


def scrape_by_date(date_str):
    events = scrape_date(date_str)

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    for event in events:

        try:

            insert_cso_into_db(c, event)

        except Exception as e:
            print('Exception: %s' % e.message)

    conn.commit()
    conn.close()


def scrape_for_range(start_date_str, end_date_str):
    logging.info("Scraping from %s to %s" % (start_date_str, end_date_str))

    iter_date = datetime.datetime.strptime(start_date_str, "%m/%d/%Y")
    end = datetime.datetime.strptime(end_date_str, "%m/%d/%Y")

    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    while iter_date <= end:
        date_str = iter_date.strftime("%m/%d/%Y")
        events = scrape_date(date_str)

        for event in events:

            try:
                # Check to see if there are overlapping times.  This should not be needed, but there are
                # several inconsistencies on the MWRD webpages
                overlapping = find_overlapping_times(c, event)
                if len(overlapping) > 0:
                    for o_event in overlapping:
                        if o_event.start == event.start and o_event.stop == event.stop:
                            continue
                        logging.error(
                            "Found overlapping overflows.  Original event is: %s\n.  Overlapping event: %s" % (
                                event.to_string(), o_event.to_string()))
                        delete_from_db(c, o_event)

                        insert_cso_into_db(c, event)
                else:
                    insert_cso_into_db(c, event)

            except Exception as e:
                logging.exception(e)

        iter_date += datetime.timedelta(days=1)

    conn.commit()
    conn.close()


def search_for_overlap(event):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    a = find_overlapping_times(c, event)
    conn.close()
    return a


scrape_for_range("01/01/2007", "07/07/2016")
