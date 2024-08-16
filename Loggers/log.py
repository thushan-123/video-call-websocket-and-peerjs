import logging
from datetime import datetime
from pytz import timezone
from Functions.function import get_sl_DateTime


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
call_log = logging.getLogger("call_log")
conference_log = logging.getLogger("conference_log")

# Set logging level
err_log.setLevel(logging.DEBUG)
app_log.setLevel(logging.DEBUG)
call_log.setLevel(logging.DEBUG)
conference_log.setLevel(logging.DEBUG)

# Create  error file
err_file = logging.FileHandler("logs/error_log.log", "a")
# Create a application log file
app_file = logging.FileHandler("logs/log.log", "a")
# Create a call log file
call_file = logging.FileHandler("logs/call.log", "a")
# Create a daily conference log file
conference_file = logging.FileHandler("logs/daily_conference_logs/"+ str(get_sl_DateTime(Date_=True)), "a")

# Create a formatter
formatter = SLformatter('%(asctime)s - %(levelname)s - %(message)s')
conference_formatter = SLformatter('%(asctime)s - %(message)s')

err_file.setFormatter(formatter)
app_file.setFormatter(formatter)
call_file.setFormatter(formatter)
conference_file.setFormatter(conference_formatter)

err_log.addHandler(err_file)
app_log.addHandler(app_file)
call_log.addHandler(call_file)
conference_log.addHandler(conference_file)
