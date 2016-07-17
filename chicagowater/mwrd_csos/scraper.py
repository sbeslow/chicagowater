import logging
import urllib2
import datetime
from bs4 import BeautifulSoup

from events import CsoEvent

mwrd_base_url = 'http://apps.mwrd.org/CSO/CSOEventSynopsisReport.aspx?passdate='


# date_str should be in the format MM/DD/YYYY
def scrape_date(date_str):
    logging.info("Scraping %s" % date_str)
    url = mwrd_base_url + date_str
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
    overflow_table = soup.find('table', id="DG1")

    if overflow_table is None:
        return []

    rows = overflow_table.findAll('tr')

    events = []
    for row_num in range(1, len(rows)):

        try:
            columns = rows[row_num].findAll('td')

            columns = [column.text for column in columns]
            start = datetime.datetime.strptime(date_str + " " + columns[2], "%m/%d/%Y %H:%M")

            stop = datetime.datetime.strptime(date_str + " " + columns[3], "%m/%d/%Y %H:%M")
            duration_split = columns[4].split(':')
            duration = 60 * int(duration_split[0]) + int(duration_split[1])

            if (start + datetime.timedelta(minutes=duration)) == stop:
                date_split = date_str.split("/")
                formatted_date = date_split[2] + "-" + date_split[0] + "-" + date_split[1]
                events.append(CsoEvent(columns[0], columns[1], formatted_date, start, stop, duration))
            else:
                maybe_end_date = start + datetime.timedelta(minutes=duration)
                maybe_end_time_str = maybe_end_date.strftime("%H:%M")
                stop_time_str = stop.strftime("%H:%M")
                if maybe_end_time_str != stop_time_str:
                    logging.error("Unable to calculate end time for row %s on %s" % (str(row_num), date_str))
                    continue
                stop = maybe_end_date

                date_iter = start
                second_day_datetime = start + datetime.timedelta(days=1)
                second_day_string = second_day_datetime.strftime("%m/%d/%Y")
                end_of_day = datetime.datetime.strptime(second_day_string + " " + "0:00", "%m/%d/%Y %H:%M")

                while end_of_day < stop:
                    formatted_date = date_iter.strftime("%Y-%m-%d")
                    new_duration = int((end_of_day-date_iter).total_seconds() / 60)

                    events.append(CsoEvent(columns[0], columns[1], formatted_date, date_iter, end_of_day, new_duration))
                    date_iter = end_of_day
                    end_of_day += datetime.timedelta(days=1)

                formatted_date = date_iter.strftime("%Y-%m-%d")
                new_duration = int((maybe_end_date-date_iter).total_seconds() / 60)
                events.append(CsoEvent(columns[0], columns[1], formatted_date, date_iter, stop, new_duration))

        except Exception as e:
            logging.error("Exception on %s row %i" % (date_str, row_num))
            logging.exception(e)

    return events
