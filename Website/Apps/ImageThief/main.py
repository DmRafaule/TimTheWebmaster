from WebCrawler.crawler import WebCrawler
from ImgScrapper.scrapper import ImgScrapper
from Utils.utils import log, initFolder, initFile, checkURL, toMinimalURL
from Utils.utils import toDomainURL, initDataFile
import config as C


def downloadAllImagesFromListPage(
        urls: [],
        noisy: bool = True) -> None:
    log("Status: Download images from list of pages.", C.LOG_FILE)
    for url in urls:
        scrapper = ImgScrapper(url, noisy)
        scrapper.scrape(url)
        scrapper.download()
    scrapper.zip()
    log(f"Result: ImageThief has successfully scrape {len(scrapper.getImgs())} images from {len(urls)} pages")


def downloadAllImagesFromPage(
        url: str = None,
        noisy: bool = True) -> None:
    log(f"Status: Download images from single page ({C.URL}).", C.LOG_FILE)
    scrapper = ImgScrapper(url, noisy)
    scrapper.scrape(url)
    scrapper.download()
    scrapper.zip()
    log(f"Result: ImageThief has successfully scrape {len(scrapper.getImgs())} images from {url} pages")


def downloadAllImagesFromSite(
        url: str = None,
        noisy: bool = True,
        mode: C.ScrappingMode = C.ScrappingMode.FULL) -> None:
    log(f"Status: Download images from whole site ({C.URL}).", C.LOG_FILE)
    spider = WebCrawler(url, noisy)
    links_to_scrapp = spider.getAllInternalLinks()

    scrapper = ImgScrapper(url, noisy)
    scrapper.scrape(*links_to_scrapp)
    scrapper.download()
    scrapper.zip()
    log(f"Result: ImageThief has successfully scrape {len(scrapper.getImgs())} images from {len(links_to_scrapp)} pages")


if __name__ == "__main__":
    initFolder(C.RESULT_FOLDER)
    if C.MODE is C.ScrappingMode.LIST_PAGES and len(C.URLS) > 0:
        C.RESULT_FOLDER += "/tmp_" + toDomainURL(C.URLS[0])
    else:
        C.RESULT_FOLDER += "/tmp_" + toDomainURL(C.URL)
    initFolder(C.RESULT_FOLDER)
    C.IMAGES_FOLDER = C.RESULT_FOLDER + "/" + C.IMAGES_FOLDER
    initFolder(C.IMAGES_FOLDER)
    C.LOG_FILE = C.RESULT_FOLDER + "/" + C.LOG_FILE
    initFile(C.LOG_FILE)
    C.DATA_FILE = C.RESULT_FOLDER + "/" + C.DATA_FILE
    initDataFile(C.DATA_JSON_TEMPLATE, C.DATA_FILE)
    log(f"""
    {C.NAME} v{C.VERSION}
    by {C.AUTHOR}
    from the website: {C.SOURCE_WEBSITE}

============================================\n""", C.LOG_FILE)
    if checkURL(C.URL):
        if C.MODE is C.ScrappingMode.FULL:
            C.URL = toMinimalURL(C.URL)
            downloadAllImagesFromSite(C.URL, C.VERBOSE, C.MODE)
        elif C.MODE is C.ScrappingMode.LIST_PAGES and len(C.URLS) > 0:
            downloadAllImagesFromListPage(C.URLS, C.VERBOSE)
        elif C.MODE is C.ScrappingMode.SINGLE_PAGE:
            downloadAllImagesFromPage(C.URL, C.VERBOSE)
    else:
        log(f"Error(checkURL): This url, {C.URL}, is invalid.")
