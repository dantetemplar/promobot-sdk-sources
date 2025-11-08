import time

MS_COEF = 1000


def get_current_time_in_milliseconds():
    return round(time.time() * MS_COEF)