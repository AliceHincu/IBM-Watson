import os
import re


def get_files_from_directory(directory):
    """
    Get all files from a directory
    """
    if not os.path.exists(directory) or not os.path.isdir(directory):
        raise RuntimeError("Folder does not exist")
    return [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]


def is_title(input):
    if input is None:
        return False
    regex = r"^\[\[(.*?)]]$"
    return re.match(regex, input) is not None


def retrieve_title(input):
    return input.strip("[]")


def is_category_line(input):
    if input is None:
        return False
    return input.startswith("CATEGORIES:")


def tokenize_category_line(input):
    return input[len("CATEGORIES: "):].split(", ")


def is_redirect_line(input):
    if input is None:
        return False
    return input.startswith("#REDIRECT ") or input.startswith("#redirect ")


def get_redirect_page_title(input):
    return input[len("#REDIRECT "):]