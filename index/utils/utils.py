import os
import re


def get_files_from_directory(directory):
    """
    Get all files from a directory
    """
    if not os.path.exists(directory) or not os.path.isdir(directory):
        raise RuntimeError("Folder does not exist")
    return [os.path.join(directory, file) for file in os.listdir(directory) if
            os.path.isfile(os.path.join(directory, file))]


def preprocess_file_content(text):
    """
    Preprocess the file content to remove template patterns, [ref][/ref] tags, and link tags along with their enclosed
    content.
    """
    template_tag_pattern = r'\[tpl\].*?\[/tpl\]'
    ref_tag_pattern = r'\[ref\].*?\[/ref\]'
    url_pattern = r'http\S+|www.\S+'

    # Remove the matched patterns from the text
    cleaned_text = re.sub(template_tag_pattern, '', text, flags=re.DOTALL)
    cleaned_text = re.sub(ref_tag_pattern, '', cleaned_text, flags=re.DOTALL)
    cleaned_text = re.sub(url_pattern, '', cleaned_text, flags=re.DOTALL)

    return cleaned_text
