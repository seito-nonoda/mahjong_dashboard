from datetime import datetime


def retrieve_date_today():
    now = datetime.now()
    today = now.strftime("%Y/%m/%d")

    return today
