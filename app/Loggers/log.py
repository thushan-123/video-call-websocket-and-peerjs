import logging
from datetime import datetime
from pytz import timezone


# Create a custom formatter to format date-time according to SL time-Zone
class SLformatter(logging.Formatter):
    def timeFormat(self, record, datefmt=None):
        sri_lanka_time = datetime.fromtimestamp(record.created, tz=timezone("Asia/Colombo"))
        if datefmt:
            s = sri_lanka_time.strftime(datefmt)
        else:
            s = sri_lanka_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        return s


# Create a Loggers -> err_log ,
err_log = logging.getLogger("err_log")
app_log = logging.getLogger("app_log")

# Set logging level
err_log.setLevel(logging.DEBUG)
app_log.setLevel(logging.DEBUG)

# Create  error file
err_file = logging.FileHandler("logs/error_log.log", "a")
app_file = logging.FileHandler("logs/log.log", "a")

# Create a formatter
formatter = SLformatter('%(asctime)s - %(levelname)s - %(message)s')

err_file.setFormatter(formatter)
app_file.setFormatter(formatter)

err_log.addHandler(err_file)
app_log.addHandler(app_file)
