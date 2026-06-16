import re


def clean_text(text):

    if not text:
        return ""

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Remove extra line breaks and tabs
    text = re.sub(r"[\r\n\t]+", " ", text)

    # Keep important technical characters
    text = re.sub(r"[^a-zA-Z0-9\s\+\#\.\-/]", " ", text)

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip() 