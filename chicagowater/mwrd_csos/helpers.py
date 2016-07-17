from database_methods import select_from_db


def find_overlapping_times(c, event):

    sql = "SELECT * FROM CSOs WHERE Date='%s' and Location='%s'" % (event.date_str, event.location)
    results = select_from_db(c, sql)
    ret_val = []
    for result in results:
        if result.start == event.start and result.stop == result.stop:
            ret_val.append(result)
            continue
        elif result.start >= event.stop or result.stop <= event.start:
            continue

        ret_val.append(result)
    return ret_val
