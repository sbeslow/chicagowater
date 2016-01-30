import urllib2
import time
from bs4 import BeautifulSoup

mwrd_base_url = 'http://apps.mwrd.org/CSO/CSOEventSynopsisReport.aspx?passdate='


# date_str should be in the format MM/DD/YYYY
def scrape_date(date_str):
    url = mwrd_base_url + date_str
    soup = BeautifulSoup(urllib2.urlopen(url).read(), "html.parser")
    overflow_table = soup.find('table', id="DG1")
    rows = overflow_table.findAll('tr')

    events = []
    for row_num in range(1, len(rows)):
        columns = rows[row_num].findAll('td')

        columns = [column.text for column in columns]
        start_time = time.strptime(date_str + " " + columns[2], "%m/%d/%Y %H:%M")
        stop_time = time.strptime(date_str + " " + columns[3], "%m/%d/%Y %H:%M")
        duration_split = columns[4].split(':')
        duration = 60 * int(duration_split[0]) + int(duration_split[1])

        date_split = date_str.split("/")
        formatted_date = date_split[2] + "-" + date_split[0] + "-" + date_split[1]
        events.append({"Location": columns[0], "Segment": columns[1], "Date": formatted_date, "StartTime": start_time,
                       "EndTime": stop_time, "Duration": duration})

    return events



