from enum import Enum
import json
import time

from bs4 import BeautifulSoup
import requests

import ImageThief.config as C
from ImageThief.Utils.utils import log, toMinimalURL, afterDomain


class LinkType(Enum):
    INTERNAL = 1
    EXTERNAL = 2


class WebCrawler:
    url = str
    domain = str
    data_file = str
    log_file = str

    def __init__(self, url: str,
                 data_file: str,
                 log_file: str,
                 noisy: bool = True):
        self.data_file = data_file
        self.log_file = log_file
        start = time.time()
        self.url = url
        current = self.__dataGetCurrentLink()
        if current == 0:
            self.__crawlSitemap(url + "/" + "sitemap.xml")
            log(f"Found {len(self.__dataGetLinks(LinkType.INTERNAL))} internal links.", self.log_file)
        links = self.__dataGetLinks(LinkType.INTERNAL)
        length = len(links)
        log("Status: Crawling links", self.log_file)
        if length == 0:
            self.__crawl(self.url)

        while True:
            links = self.__dataGetLinks(LinkType.INTERNAL)
            length = len(links)

            for link in links[current:]:
                self.__crawl(self.url + link["url"])
            if current == length:
                break

            current = self.__dataGetCurrentLink()

        end = time.time()
        log(f"Result: Total internal links ({len(self.__dataGetLinks(LinkType.INTERNAL))})", self.log_file)
        log(f"Result: Total external links ({len(self.__dataGetLinks(LinkType.EXTERNAL))})", self.log_file)
        log(f"Result: Total crawling execution time ({end - start}) sec..", self.log_file)

    def __crawl(self, url: str):
        status = "Ok"
        try:
            if self.__crawlable(url):
                page = requests.get(url, headers=C.HEADERS, timeout=1, verify=False)
            else:
                raise NotImplementedError
        except requests.exceptions.HTTPError as e:
            log(f"Error: {e.args[0]}.", self.log_file)
            status = "NotOk"
        except requests.exceptions.ReadTimeout:
            log("Error: Time out.", self.log_file)
            status = "NotOk"
        except requests.exceptions.ConnectionError as e:
            log(f"Error: Something wrong with connection. {e}", self.log_file)
            status = "NotOk"
        except requests.exceptions.RequestException as e:
            log(f"Error: While trying make request. {e}", self.log_file)
            status = "NotOk"
        except NotImplementedError:
            log("Error: Could parse file with such extention name.", self.log_file)
            status = "NotOk"
        else:
            soup = BeautifulSoup(page.text, 'lxml')
            for link in soup.find_all("a"):
                # Does our link even has 'href' attribute and it is not 'anchor' link
                if link.has_attr('href') and "#" not in link['href']:
                    # We check again, on does it crawlable to deserve a chanse to 
                    # be inserted indo database
                    if self.__crawlable(link["href"]):
                        if link['href'].startswith(('/')):
                            self.__dataLinkInsert(link['href'], LinkType.INTERNAL, page.status_code)
                        else:
                            if link['href'].startswith((self.url, self.url.replace("https", "http"), self.url.replace("http", "https"))):
                                self.__dataLinkInsert(link['href'].replace(self.url, ""), LinkType.INTERNAL, page.status_code)
                            else:
                                if link['href'].startswith(("https://", "http://")):
                                    self.__dataLinkInsert(link['href'], LinkType.EXTERNAL, page.status_code)
        finally:
            self.__dataSetCurrentLink(self.__dataGetCurrentLink() + 1)
            current = self.__dataGetCurrentLink()
            log(f"{status}: Crawled {current}/{self.__dataGetLinkNumber()} {url}", self.log_file)

    # Walk through sitemap file
    def __crawlSitemap(self, sitemap: str):
        status = "Ok"
        log("Status: Checking sitemap", self.log_file)
        try:
            if self.__crawlable(sitemap):
                page = requests.get(url=sitemap, headers=C.HEADERS, timeout=1, verify=False)
            else:
                # Maybe make your own Exception class
                raise NotImplementedError
        except requests.exceptions.HTTPError as e:
            log(f"Error: {e.args[0]}.", self.log_file)
            status = "NotOk"
        except requests.exceptions.ReadTimeout as e:
            log(f"Error: Time out. {e}", self.log_file)
            status = "NotOk"
        except requests.exceptions.ConnectionError as e:
            log(f"Error: Something wrong with connection. {e}", self.log_file)
            status = "NotOk"
        except requests.exceptions.RequestException as e:
            log(f"Error: While trying make request. {e}", self.log_file)
            status = "NotOk"
        except NotImplementedError:
            log("Error: Could parse file with such extention name.", self.log_file)
            status = "NotOk"
        else:
            soup = BeautifulSoup(page.text, 'xml')
            for sm in soup.find_all('loc'):
                if ".xml" in sm.text:
                    log(f"{status}ey: New sub sitemap ({sm.text})", self.log_file)
                    self.__crawlSitemap(sm.text)
                else:
                    self.__dataLinkInsert(sm.text.replace(self.url, ""), LinkType.INTERNAL, page.status_code)

    def __crawlable(self, url: str) -> bool:
        notcrawlable_ext = (
            ".zip",
            ".mp4",
            ".mp3",
            ".js",
            ".css",
            ".tar",
            ".7z",
            ".png",
            ".jpg",
            ".webp",
            ".svg",
            ".gz",
            ".ico",
            ".pdf",
            ".fp2",
            ".epub",
            ".txt",
        )
        if url.endswith(notcrawlable_ext):
            return False
        return True

    def __dataClenUpDuplicates(self):
        log("Remove duplicated urls.", self.log_file)
        with open(self.data_file, "r", encoding="utf-8") as F:
            links = json.load(F)
            # Remove duplicates by converting list to set and then back to list again
            links[self.__linkTypeToStr(LinkType.INTERNAL)] = list(set(links[self.__linkTypeToStr(LinkType.INTERNAL)]))
        with open(self.data_file, "w", encoding="utf-8") as F:
            json.dump(links, F, indent=2)

    def __dataIsEmpty(self) -> bool:
        type = self.__linkTypeToStr(LinkType.INTERNAL)
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            if data[type]:
                log("Data file is not empty", self.log_file)
                return False
            else:
                log("Data file is empty", self.log_file)
                return True

    def __dataGetLinks(self, type: LinkType) -> []:
        type = self.__linkTypeToStr(type)
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            return data[type]

    def __dataGetCurrentLink(self) -> int:
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            return data["current_link_to_crawl"]

    def __dataSetCurrentLink(self, index: int):
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            data["current_link_to_crawl"] = index
        with open(self.data_file, "w", encoding="utf-8") as F:
            json.dump(data, F, indent=2)

    def __dataGetLinkNumber(self) -> int:
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            return data['links_number']

    def __dataLinkInsert(self, link: str, type: LinkType, status_code: int):
        # Before use type var. It is neccessary to convert it to string
        type = self.__linkTypeToStr(type)
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            for dataLink in data[type]:
                if link == dataLink['url']:
                    break
            else:
                log(f"Found new link ({link})", self.log_file)
                if type == self.__linkTypeToStr(LinkType.INTERNAL):
                    data["links_number"] += 1
                data[type].append({
                    'url': link,
                })
                with open(self.data_file, "w", encoding="utf-8") as Fw:
                    # Make sure that data will be dumped. 
                    # Sometime Keyboard interruption break a data file
                    try:
                        json.dump(data, Fw, indent=2)
                    except Exception:
                        json.dump(data, Fw, indent=2)

    def __linkTypeToStr(self, ltype: LinkType) -> str:
        result = ""
        if LinkType.INTERNAL == ltype:
            result = "internal_links"
        else:
            result = "external_links"
        return result

    def getAllInternalLinks(self) -> dict:
        return self.__dataGetLinks(LinkType.INTERNAL)

    def getAllExternalLinks(self) -> dict:
        return self.__dataGetLinks(LinkType.EXTERNAL)
