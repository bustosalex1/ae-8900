"""General utilities."""
import logging
import re


def safe_string(input_string: str) -> str:
    """
    Remove characters from an input string that... might be unsafe when using mkdir.

    :param input_string: the unsanitized string
    :return: the updated string
    """
    output_string = re.sub("[^A-Za-z0-9\_\-]", "", input_string)

    return output_string


def initialize_logging(log_level: int = logging.DEBUG) -> None:
    """Set up logging with a ColorLogFormatter."""
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(log_level)
    stdout_handler.setFormatter(ColorLogFormatter())
    logging.basicConfig(handlers=[stdout_handler], level=log_level)


class ColorLogFormatter(logging.Formatter):
    """I just want colors in my log messages."""

    blue = "\x1b[34m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self) -> None:
        """Create a new ColorLogFormatter."""
        super().__init__()
        self.FORMATS = {
            logging.DEBUG: f"{self.blue}[ %(levelname)s ]\t%(name)s{self.reset}:\t%(message)s",
            logging.INFO: f"{self.green}[ %(levelname)s ]\t%(name)s{self.reset}:\t%(message)s",
            logging.WARNING: f"{self.yellow}[ %(levelname)s ]\t%(name)s{self.reset}:\t%(message)s",
            logging.ERROR: f"{self.red}[ %(levelname)s ]\t%(name)s{self.reset}:\t%(message)s",
            logging.CRITICAL: f"{self.bold_red}[ %(levelname)s ]\t%(name)s{self.reset}:\t%(message)s",
        }

    def format(self, record: logging.LogRecord):
        """Just extending the base class."""
        formatter = logging.Formatter(self.FORMATS.get(record.levelno))
        return formatter.format(record)
