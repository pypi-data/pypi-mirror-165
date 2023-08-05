# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta


def after_timestamp(milliseconds=0):
    after_datetime = datetime.now() + timedelta(milliseconds=milliseconds)
    return datetime_to_timestamp(after_datetime)


def datetime_to_timestamp(datetimeval: datetime):
    timetuple = datetimeval.timetuple()
    return int(round(time.mktime(timetuple) * 1000) + datetimeval.microsecond/1000)
