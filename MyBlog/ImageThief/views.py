import os
import time
#import ctypes # Only used on Windows
from threading import Thread

from django.http import JsonResponse
from django.shortcuts import render
from Main.utils import initDefaults
from MyBlog import settings
from django.utils.translation import gettext_lazy as _

from .WebCrawler.crawler import WebCrawler
from .ImgScrapper.scrapper import ImgScrapper
from .Utils.utils import log, initFolder, initFile, checkURL, toMinimalURL, checkIsListURLs, extractURLs
from .Utils.utils import toDomainURL, initDataFile
import ImageThief.config as C


TRY_LIMIT = 1000
REQUEST_LAG = 5
TIME_BERFORE_CLEANUP = 3600


def tool_main(request):
    request.session[f"inWork_{request.session.session_key}"] = False
    try_limit = request.session["user_tries_limit"] = request.session.get(f"user_tries_limit", TRY_LIMIT)
    tries_counter = request.session[f"user_tries_{request.session.session_key}"] = request.session.get(f"user_tries_{request.session.session_key}", 1)

    context = initDefaults(request)
    context.update({'try_limit': try_limit})
    context.update({'tries_counter': tries_counter})
    context.update({'archive': os.path.join('tools', C.SLUG, 'archive.zip') })

    return render(request, 'ImageThief/image_thief.html', context=context)

# This is how you will kill a thread if thread function target is not a loop-base one
def killProcess(pid: int) -> None:
    try:
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(pid,
            ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(pid, 0)
            print('Exception raise failure')
    except:
        log(f"Error: Could not kill {pid} process.")
    else:
        log(f"Ok: Killed {pid} process.")

def downloadAllImagesFromListPage(
        urls: [],
        data_file: str,
        log_file: str,
        images_folder: str,
        result_folder: str,
        noisy: bool = True) -> None:
    log("Mode: Download images from list of pages.", log_file)
    for url in urls:
        scrapper = ImgScrapper(url, data_file, log_file, images_folder, result_folder,  noisy)
        scrapper.scrape(url)
        scrapper.download()
    scrapper.zip()
    log("Status: Finishing", log_file)
    log(f"Result: ImageThief has successfully scrape {len(scrapper.getImgs())} images from {len(urls)} pages", log_file)

def downloadAllImagesFromPage(
        url: str,
        data_file: str,
        log_file: str,
        images_folder: str,
        result_folder: str,
        noisy: bool = True) -> None:
    log(f"Mode: Download images from single page ({url}).", log_file)
    scrapper = ImgScrapper(url, data_file, log_file, images_folder, result_folder, noisy)
    scrapper.scrape(url)
    scrapper.download()
    scrapper.zip()
    log("Status: Finishing", log_file)
    log(f"Result: ImageThief has successfully scrape {len(scrapper.getImgs())} images from {url} pages", log_file)

def downloadAllImagesFromSite(
        url: str,
        data_file: str,
        log_file: str,
        images_folder: str,
        result_folder: str,
        noisy: bool = True,
        mode: C.ScrappingMode = C.ScrappingMode.FULL) -> None:
    log(f"Mode: Download images from whole site ({url}).", log_file)
    spider = WebCrawler(url, data_file, log_file, noisy)
    links_to_scrapp = spider.getAllInternalLinks()

    scrapper = ImgScrapper(url, data_file, log_file, images_folder, result_folder, noisy)
    scrapper.scrape(*links_to_scrapp)
    scrapper.download()
    scrapper.zip()
    log("Status: Finishing", log_file)
    log(f"Result: ImageThief has successfully scrape {len(scrapper.getImgs())} images from {len(links_to_scrapp)} pages", log_file)

def startProcess(request):
    user_id = request.session.session_key
    url = request.GET["url"]
    urls = extractURLs(url)
    mode = request.GET["mode"]
    log_file = request.session[f"log_file_{user_id}"]
    data_file = request.session[f"data_file_{user_id}"]
    images_folder = request.session[f"image_folder_{user_id}"]
    result_folder = request.session[f"result_folder_{user_id}"]
    if mode == "full":
        mode = C.ScrappingMode.FULL
        downloadAllImagesFromSite(url, data_file, log_file, images_folder, result_folder, C.VERBOSE, mode)
    elif mode == "list-pages":
        mode = C.ScrappingMode.LIST_PAGES
        downloadAllImagesFromListPage(urls, data_file, log_file, images_folder, result_folder, C.VERBOSE)
    else:
        mode = C.ScrappingMode.SINGLE_PAGE
        downloadAllImagesFromPage(url, data_file, log_file, images_folder, result_folder, C.VERBOSE)

# Timer which gonna let user use it only after some period of time
def timerTillNewRequestsAvailable(request, tim: int):
    time.sleep(tim)
    request.session[f"user_istried_{request.session.session_key}"] = False
    request.session.save()

def start(request):
    data = {}
    user_id = request.session.session_key
    status = 200
    request.session[f"current_log_line_{user_id}"] = 0
    try_limit = request.session[f"user_tries_limit"]
    tries_counter = request.session[f"user_tries_{user_id}"]
    isTried = request.session.get(f"user_istried_{user_id}")
    if tries_counter <= try_limit and tries_counter >= 1 and not isTried:
        startProcessProcess = Thread(target=startProcess, args=(request,))
        try:
            startProcessProcess.start()
            # Save a process pid for earlier closing (like tab, window)
            request.session[f"process_{user_id}"] = startProcessProcess.native_id
            request.session[f"inWork_{user_id}"] = True
            request.session[f"user_istried_{user_id}"] = True
            request.session.save()
            # Max time of execution 1 hour
            startProcessProcess.join(timeout=3600)  # 1 hour
            # Start timer
            timer = Thread(target=timerTillNewRequestsAvailable, args=(request, REQUEST_LAG), daemon=True)
            timer.start()
            exitCode = True
            startProcessProcess.close()
        except Exception as ex:
            exitCode = False
        else:
            exitCode = False
        tries_counter += 1
        request.session[f"user_tries_{user_id}"] = tries_counter
        request.session.save()
        imgs = os.path.join(request.session[f"result_folder_{user_id}"], "imgs.zip")
        imgs = imgs[imgs.find(os.path.join(settings.MEDIA_URL.replace('/',''),C.RESULT_FOLDER)) - 1:]
        data = {
            "btn": _("Ещё раз"),
            "imgs_path": imgs,
            "try": tries_counter,
            "try_limit": try_limit,
        }
        # If user stoped a tool, will return error code
        if exitCode:
            data["btn"] = _("Начать")
            status = 406
    else:
        data = {
            "btn": _("Начать"),
            "status_msg": _("Не так быстро ковбой, подожди 5 секунд"),
            "try": tries_counter,
            "try_limit": try_limit,
        }
        status = 406

    return JsonResponse(data, status=status)


def init(request):
    user_id = request.session.session_key
    request.session["user_tries_limit"] = request.session.get(f"user_tries_limit", TRY_LIMIT)
    request.session[f"user_tries_{user_id}"] = request.session.get(f"user_tries_{user_id}", 1)
    request.session[f"user_istried_{user_id}"] = request.session.get(f"user_istried_{user_id}", False)
    url = request.GET["url"]
    mode = request.GET["mode"]
    if mode == "full":
        MODE = C.ScrappingMode.FULL
    elif mode == "list-pages":
        MODE = C.ScrappingMode.LIST_PAGES
    else:
        MODE = C.ScrappingMode.SINGLE_PAGE
    btn = _("Стоп")
    status_msg = ""
    status = 200
    URLS = []
    URL = url
    # Define which function to use
    # It depends on selected mode, by user
    if checkIsListURLs(url):
        URLS = extractURLs(url)
        for u in URLS:
            result = checkURL(u)
            if not result["status"]:
                status_msg = result["msg"]
                status_msg += f"({u})"
                status = 500
                log(status_msg)
                return JsonResponse({
                    "btn": btn,
                    "status_msg": status_msg
                    }, status=status)
        if MODE is C.ScrappingMode.LIST_PAGES:
            if len(URLS) <= 1:
                status_msg = _("Ошибка: Слишком мало адресов. Добавь хотябы 2.")
                status = 500
                log(status_msg)
                return JsonResponse({
                    "btn": btn,
                    "status_msg": status_msg
                    }, status=status)
        else:
            status_msg = _("Ошибка: Ты выбрал не правильный режим для списка страниц")
            status = 500
            log(status_msg)
            return JsonResponse({
                "btn": btn,
                "status_msg": status_msg
                }, status=status)
    else:
        result = checkURL(URL)
        if result["status"]:
            if MODE is C.ScrappingMode.FULL:
                URL = toMinimalURL(URL)
        else:
            status_msg = result["msg"]
            status = 500
            log(status_msg)
            return JsonResponse({
                "btn": btn,
                "status_msg": status_msg
                }, status=status)
    # Init result folder
    # Which gonna consist from main, top lever folder
    # Then folder by user session key
    # Then folder by website domain name
    RESULT_FOLDER = os.path.join(settings.MEDIA_ROOT, C.RESULT_FOLDER)
    initFolder(RESULT_FOLDER)
    if MODE is C.ScrappingMode.LIST_PAGES and len(URLS) > 1:
        RESULT_FOLDER = os.path.join(RESULT_FOLDER, "user_" + str(user_id))
        initFolder(RESULT_FOLDER)
        RESULT_FOLDER = os.path.join(RESULT_FOLDER, "website_" + toDomainURL(toMinimalURL(URLS[0])) + "-list_pages")
        request.session[f"result_folder_{user_id}"] = RESULT_FOLDER
        initFolder(RESULT_FOLDER)
    elif MODE is C.ScrappingMode.SINGLE_PAGE:
        RESULT_FOLDER = os.path.join(RESULT_FOLDER, "user_" + str(user_id))
        initFolder(RESULT_FOLDER)
        RESULT_FOLDER = os.path.join(RESULT_FOLDER, "website_" + toDomainURL(toMinimalURL(URL)) + "-single_page")
        request.session[f"result_folder_{user_id}"] = RESULT_FOLDER
        initFolder(RESULT_FOLDER)
    else:
        RESULT_FOLDER = os.path.join(RESULT_FOLDER, "user_" + str(user_id))
        initFolder(RESULT_FOLDER)
        RESULT_FOLDER = os.path.join(RESULT_FOLDER, "website_" + toDomainURL(toMinimalURL(URL)) + "-full")
        request.session[f"result_folder_{user_id}"] = RESULT_FOLDER
        initFolder(RESULT_FOLDER)
    # Init images folder
    IMAGES_FOLDER = os.path.join(RESULT_FOLDER, C.IMAGES_FOLDER)
    request.session[f"image_folder_{user_id}"] = IMAGES_FOLDER
    initFolder(IMAGES_FOLDER)
    # Init logger file
    LOG_FILE = os.path.join(RESULT_FOLDER, C.LOG_FILE)
    request.session[f"log_file_{user_id}"] = LOG_FILE
    initFile(LOG_FILE)
    # Init data file
    DATA_FILE = os.path.join(RESULT_FOLDER, C.DATA_FILE)
    request.session[f"data_file_{user_id}"] = DATA_FILE
    initDataFile(C.DATA_JSON_TEMPLATE, DATA_FILE)

    log(f"""
    {C.NAME} v{C.VERSION}
    by {C.AUTHOR}
    from the website: {C.SOURCE_WEBSITE}

============================================\n""", LOG_FILE)

    return JsonResponse({
        "btn": btn,
        "url": URL,
        "mode": mode,
        "status_msg": status_msg
        }, status=status)


def stop(request):
    status = 200
    try:
        killProcess(request.session[f"process_{request.session.session_key}"])
    except Exception:
        pass

    btn = _("Начать")
    return JsonResponse({
        "btn": btn,
        }, status=status)


def update_status(request):
    data = {
        "period": "Crawling",
    }
    status = 200
    user_id = request.session.session_key
    with open(request.session[f"log_file_{user_id}"], "r", encoding="utf-8") as F:
        text: str = F.read()
        start = text.rfind("Status")
        start_period = text.find(" ", start) + 1
        end_period = text.find("\n", start_period)
        data["period"] = text[start_period:end_period]
    return JsonResponse(data, status=status)

def update_logs(request):
    status = 200
    if request.session[f"inWork_{request.session.session_key}"]:
        data = {"msg": ""}
        user_id = request.session.session_key
        current_line = request.session[f"current_log_line_{user_id}"]
        line_number = 0

        with open(request.session[f"log_file_{user_id}"], "r", encoding="utf-8") as F:
            content = F.read()
            line_number = content.count("\n")

        lines = ""
        with open(request.session[f"log_file_{user_id}"], "r", encoding="utf-8") as F:
            # To store lines
            for i, line in enumerate(F):
                # read line 4 and 7
                if i in range(current_line, line_number):
                    lines += line
                request.session[f"current_log_line_{user_id}"] = i + 1
            data["msg"] = lines
        request.session.save()
        data["msg_er"] = ""
    else:
        data = {"msg_er": _("Нечего отображать. Запусти парсинг.")}
    return JsonResponse(data, status=status)
