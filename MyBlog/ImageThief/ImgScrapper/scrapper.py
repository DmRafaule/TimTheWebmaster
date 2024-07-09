import os
import time
import random
import string
import json
from zipfile import ZipFile, ZIP_DEFLATED

from bs4 import BeautifulSoup
import requests

import ImageThief.config as C
from ImageThief.Utils.utils import toDomainURL, toMinimalURL, log


def GetRandomString(length: int) -> str:
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


class ImgScrapper:
    url = str
    domain = str
    min_url = str
    data_file = str
    log_file = str
    images_folder = str
    result_folder = str

    def __init__(self,
                 url: str,
                 data_file: str,
                 log_file: str,
                 images_folder: str,
                 result_folder: str,
                 noisy: bool = True):
        self.url = url
        self.min_url = toMinimalURL(url)
        self.domain = toDomainURL(url)
        self.data_file = data_file
        self.log_file = log_file
        self.images_folder = images_folder
        self.result_folder = result_folder

    def scrape(self, *urls):
        start = time.time()
        status = "Ok"

        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            data["links_number"] = len(urls)
            data["internal_links"] = urls
        with open(self.data_file, "w", encoding="utf-8") as F:
            json.dump(data, F, indent=2)

        log("Status: Scrapping images", self.log_file)
        length = len(urls)
        for link in urls[self.__dataGetCurrentLink():]:
            if type(link) is not str:
                l_url = link["url"]
            else:
                l_url = link
            current = self.__dataGetCurrentLink()
            try:
                if type(link) is not str:
                    page = requests.get(self.url + l_url, headers=C.HEADERS, verify=False)
                else:
                    page = requests.get(l_url, headers=C.HEADERS, verify=False)
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
            else:
                log(f"{status}: Scraped {current+1}/{length} ({l_url})", self.log_file)
                soup = BeautifulSoup(page.text, 'lxml')
                for img_tag in soup.find_all('img'):
                    if img_tag.has_attr('src'):
                        if img_tag['src'].startswith(("http")):
                            img_path = img_tag['src']
                        else:
                            img_path = self.min_url + img_tag['src']

                        for img_one in self.__dataGetImgs():
                            if img_tag['src'] in img_one:
                                break
                        else:
                            self.__dataImgInsert(img_path, 200)
                self.__dataSetCurrentLink(self.__dataGetCurrentLink() + 1)
        end = time.time()
        log(f"Result: Total scraping execution time ({end - start}) sec..", self.log_file)
        log(f"Result: Total scrapped images {self.__dataGetImgsNumber()} in {self.__dataGetPageNumber()} pages", self.log_file)
        self.__dataSetCurrentLink(0)

    def download(self):
        log("Status: Downloading images", self.log_file)
        # Make a slice of list of images
        imgs = self.__dataGetImgs()[self.__dataGetCurrentImg():]
        max_img_name_length = 50
        for img_path in imgs:
            try:
                img = requests.get(img_path, headers=C.HEADERS, verify=False)
                status = "Ok"
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
            else:
                current = self.__dataGetCurrentImg()
                length = self.__dataGetImgsNumber()
                filename = img_path[img_path.rfind("/"):]
                filename = filename[:max_img_name_length]
                with open(self.images_folder + "/" + filename, "wb") as F:
                    log(f"{status}: Downloaded {current+1}/{length}  {filename}", self.log_file)
                    F.write(img.content)
                    self.__dataSetCurrentImg(current + 1)

    def zip(self) -> str:
        log("Status: Archiving", self.log_file)
        filenames = next(os.walk(self.images_folder), (None, None, []))[2]
        num = len(filenames)
        with ZipFile(os.path.join(self.result_folder, C.ARCHIVE_FILE), "w", ZIP_DEFLATED) as Z:
            for i, file in enumerate(filenames):
                full_filename = os.path.join(self.images_folder, file)
                log(f"Ok: Archived {i+1}/{num} {file}", self.log_file)
                Z.write(full_filename, file)

    def getImgs(self) -> []:
        return self.__dataGetImgs()

    def __dataGetPageNumber(self) -> int:
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            return data['links_number']

    def __dataGetImgsNumber(self) -> int:
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            return data['imgs_number']

    def __dataGetImgs(self) -> []:
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            return data['imgs']

    def __dataGetCurrentImg(self) -> int:
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            return data["current_img"]

    def __dataSetCurrentImg(self, index: int):
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            data["current_img"] = index
        with open(self.data_file, "w", encoding="utf-8") as F:
            json.dump(data, F, indent=2)

    def __dataGetCurrentLink(self) -> int:
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            return data["current_link_to_scrape"]

    def __dataSetCurrentLink(self, index: int):
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            data["current_link_to_scrape"] = index
        with open(self.data_file, "w", encoding="utf-8") as F:
            json.dump(data, F, indent=2)

    def __dataImgInsert(self, link: str, status_code: int):
        with open(self.data_file, "r", encoding="utf-8") as F:
            data = json.load(F)
            for dataLink in data["imgs"]:
                if link == dataLink:
                    break
            else:
                log(f"Found new img ({link})", self.log_file)
                data["imgs_number"] = data["imgs_number"] + 1
                data["imgs"].append(link)
                with open(self.data_file, "w", encoding="utf-8") as Fw:
                    # Make sure that data will be dumped.
                    # Sometime Keyboard interruption break a data file
                    try:
                        json.dump(data, Fw, indent=2)
                    except Exception:
                        json.dump(data, Fw, indent=2)
