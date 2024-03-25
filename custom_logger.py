import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    green = "\x1b[32;20m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    resp_format = "%(asctime)s - Analyst: \n%(message)s \n"
    warning_format = "%(asctime)s - WARNING: \n%(message)s \n"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + resp_format + reset,
        logging.WARNING: yellow + warning_format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)