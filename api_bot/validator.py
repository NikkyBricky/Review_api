from urllib.parse import urlparse


def uri_validator(link):
    try:
        result = urlparse(link)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def difficulty_validator(difficulty):
    if not difficulty.isdigit():
        return False

    difficulty = int(difficulty)
    if difficulty < 1 or difficulty > 10:
        return False

    return True
