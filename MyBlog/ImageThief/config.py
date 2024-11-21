from enum import Enum


class ScrappingMode(Enum):
    # Scrape full website, without exceptions `URL and everything it can find
    FULL = 0,
    # Scrape only single page `URL
    SINGLE_PAGE = 1,
    # Scrape list of pages `URLS
    LIST_PAGES = 2

# Self slug
SLUG = "image_thief"
# Target URL
URL = ""
# List of URLS (ignored if ScrappingMode not `LIST_PAGES)
URLS = [
]
# Mode in which this script gonna work
MODE = ScrappingMode.LIST_PAGES
# Is program gonna make a lot of output to terminal ?
VERBOSE = True
# Headers for parser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "identify",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
}
# Where results will be found
RESULT_FOLDER = "tools/image_thief"
# Folder for Images
IMAGES_FOLDER = "imgs"
# Where logs stored,
LOG_FILE = "log.txt"
# Where all data stored
DATA_FILE = "data.json"
# Where all proxies stored
PROXY_FILE = "proxies.json"
# Compressed images
ARCHIVE_FILE = "imgs.zip"
# Name of program
NAME = "ImageStealer"
# Version of program
VERSION = "09"
# Creator of this program
AUTHOR = "Tim the Webmaster"
# Where it can be found
SOURCE_WEBSITE = "https://timthewebmaster.com"
# Template to init when creating DATA_FILE
DATA_JSON_TEMPLATE = {
    "version": VERSION,
    "target": URL,
    "current_link_to_crawl": 0,
    "links_number": 0,
    "external_links": [],
    "internal_links": [],
    "current_link_to_scrape": 0,
    "current_img": 0,
    "imgs_number": 0,
    "imgs": [],
}
