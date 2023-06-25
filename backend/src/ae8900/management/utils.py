"""General utilities that I don't think have a better place to be right now."""
import re


def safe_string(input_string: str) -> str:
    """
    Remove characters from an input string that... might be unsafe when using mkdir.

    :param input_string: the unsanitized string
    :return: the updated string
    """
    output_string = re.sub("[^A-Za-z0-9\_\-]", "", input_string)

    return output_string
