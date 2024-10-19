import logging
from datetime import datetime
from pytz import timezone
from Functions.function import get_sl_DateTime
import os


# Create a custom formatter to format date-time according to SL time-Zone
class SLformatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        sri_lanka_time = datetime.fromtimestamp(record.created, tz=timezone("Asia/Colombo"))
        if datefmt:
            s = sri_lanka_time.strftime(datefmt)
        else:
            s = sri_lanka_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        return s


# Global variable to track current date
current_date = None
conference_file = None


# Function to update log file if the date changes
def update_conference_log_file():
    global current_date, conference_file

    # Get current SL date
    sl_now = datetime.now(timezone("Asia/Colombo")).strftime("%Y-%m-%d")

    # If the date has changed, update the file handler
    if current_date != sl_now:
        current_date = sl_now
        if conference_file:
            conference_log.removeHandler(conference_file)
        log_file_path = f"logs/daily_conference_logs/{current_date}.log"

        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        conference_file = logging.FileHandler(log_file_path, "a")
        conference_formatter = SLformatter('%(asctime)s - %(message)s')
        conference_file.setFormatter(conference_formatter)
        conference_log.addHandler(conference_file)


# Create Loggers -> err_log, app_log, call_log, conference_log
err_log = logging.getLogger("err_log")
app_log = logging.getLogger("app_log")
call_log = logging.getLogger("call_log")
conference_log = logging.getLogger("conference_log")

# Set logging level
err_log.setLevel(logging.DEBUG)
app_log.setLevel(logging.DEBUG)
call_log.setLevel(logging.DEBUG)
conference_log.setLevel(logging.DEBUG)

# Create other log files
err_file = logging.FileHandler("logs/error_log.log", "a")
app_file = logging.FileHandler("logs/log.log", "a")
call_file = logging.FileHandler("logs/call.log", "a")

# Create a formatter
formatter = SLformatter('%(asctime)s - %(levelname)s - %(message)s')

# Apply formatter
err_file.setFormatter(formatter)
app_file.setFormatter(formatter)
call_file.setFormatter(formatter)

err_log.addHandler(err_file)
app_log.addHandler(app_file)
call_log.addHandler(call_file)

# Ensure the conference log is updated before every log write
update_conference_log_file()


# Example function to log conference details
def log_conference(message):
    update_conference_log_file()
    conference_log.info(message)


