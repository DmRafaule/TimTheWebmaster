import os
import re
import json
import hashlib
import requests
import functools
from urllib.parse import urlparse
from Apps.ImageThief.config import VERBOSE, HEADERS


def removeFile(filename: str) -> None:
    if os.path.exists(filename):
        os.remove(filename)

def initFile(filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as F:
        F.write("")


def initFolder(filename: str) -> None:
    if not os.path.exists(filename):
        os.mkdir(filename)


def initDataFile(data: any, filename: str) -> None:
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as F:
            json.dump(data, F, indent=2)


def checkIsListURLs(url: str) -> bool:
    if url.find(",") != -1:
        return True
    else:
        return False


def extractURLs(url: str) -> []:
    urls = []
    for u in url.split(","):
        urls.append(u.strip())
    return urls


def checkURL(url: str) -> bool:
    # Check if url is valid
    try:
        requests.get(url, headers=HEADERS, verify=False)
    except requests.exceptions.HTTPError as e:
        msg = f"Error: {e.args[0]}."
        return {"status": False, "msg": msg}
    except requests.exceptions.ReadTimeout:
        msg = "Error: Time out."
        return {"status": False, "msg": msg}
    except requests.exceptions.ConnectionError as e:
        msg = f"Error: Something wrong with connection. {e}"
        return {"status": False, "msg": msg}
    except requests.exceptions.RequestException as e:
        msg = f"Error: While trying make request. {e}"
        return {"status": False, "msg": msg}
    else:
        regex = '^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$'
        r = re.compile(regex)
        if re.search(r, url):
            return {"status": True, "msg": ""}
        else:
            msg = "Ошибка: Не совпадает с общим паттерном URL"
            return {"status": False, "msg": msg}


def toMinimalURL(url: str) -> bool:
    # Remove from string any unneccesary strings
    end = url.find(".")
    end = url.find("/", end)
    if end == -1:
        end = len(url)
    url = url[:end]
    return url


def afterDomain(url: str) -> bool:
    end = url.find(".")
    end = url.find("/", end)
    if end == -1:
        return "/"
    url = url[end:]
    return url


def toDomainURL(url: str) -> str:
    return urlparse(url).netloc


if VERBOSE:
    def log(message: str, file: str = None):
        if file is not None:
            with open(file, "a", encoding="utf-8") as F:
                F.write(message)
                F.write("\n")

    def debug(message: str = "", file: str = None):
        def decorator_repeat(func):
            @functools.wraps(func)
            def wrapper_debug(*args, **kwargs):
                log(message, file)
                value = func(*args, **kwargs)
                return value
            return wrapper_debug
        return decorator_repeat
else:
    def log(message: str, file: str = None):
        if file is not None:
            with open(file, "a", encoding="utf-8") as F:
                F.write(message)
                F.write("\n")

    def debug(message="", file=None):
        def decorator_repeat(func):
            @functools.wraps(func)
            def wrapper_debug(*args, **kwargs):
                value = func(*args, **kwargs)
                return value
            return wrapper_debug
        return decorator_repeat


def hash_file(filename):
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename,'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
    # return the hex representation of digest
    return h.hexdigest()
