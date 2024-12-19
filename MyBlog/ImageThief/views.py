import os
import json
from threading import Thread

from django.http import JsonResponse
from django.template import loader
from django.template.response import TemplateResponse
from django.shortcuts import render
from Main.utils import initDefaults
from MyBlog import settings
from django.utils.translation import gettext_lazy as _

import Main.utils as U
import Post.views as P
from Post.models import Note, Tag
from .WebCrawler.crawler import WebCrawler
from .ImgScrapper.scrapper import ImgScrapper
from .Utils.utils import log, initFolder, initFile, checkURL, toMinimalURL, checkIsListURLs, extractURLs
from .Utils.utils import toDomainURL, initDataFile, removeFile
import ImageThief.config as C


TRY_LIMIT = 1000
REQUEST_LAG = 5
TIME_BERFORE_CLEANUP = 3600
MAX_NOTES_ON_TOOL = 3


def tool_main(request):
    request.session[f"inWork_{request.session.session_key}"] = False

    context = initDefaults(request)
    context.update({'archive': os.path.join('tools', C.SLUG, 'archive.zip') })
    context.update({'proxies_example': os.path.join('tools', C.SLUG, 'proxies.json') })

    # Get latest notes about ImageThief
    imageThief_tags = Tag.objects.filter(slug_en='imagethief')
    if len(imageThief_tags) > 0:
        posts = P.filterByTag(Note.objects.filter(isPublished=True), [imageThief_tags[0]])[:MAX_NOTES_ON_TOOL]
        context.update({'imageThief_tag': imageThief_tags[0].slug})
        context.update({'posts': posts})
        loaded_template = loader.get_template(f'Post/basic--post_preview-note.html')
        context.update({'latest_notes': loaded_template.render(context, request)})

    return TemplateResponse(request, 'ImageThief/image_thief.html', context=context)

def downloadAllImagesFromListPage(
        urls: [],
        data_file: str,
        log_file: str,
        proxy_file: str,
        images_folder: str,
        result_folder: str,
        isDynamic: bool,
        noisy: bool = True) -> None:
    log("Mode: Download images from list of pages.", log_file)
    for url in urls:
        scrapper = ImgScrapper(url, data_file, log_file, proxy_file, images_folder, result_folder, isDynamic, noisy)
        scrapper.scrape(url)
        scrapper.download()
    scrapper.zip()
    log("Status: Finishing", log_file)
    log(f"Result: ImageThief has successfully scrape {len(scrapper.getImgs())} images from {len(urls)} pages", log_file)

def downloadAllImagesFromPage(
        url: str,
        data_file: str,
        log_file: str,
        proxy_file: str,
        images_folder: str,
        result_folder: str,
        isDynamic: bool,
        noisy: bool = True) -> None:
    log(f"Mode: Download images from single page ({url}).", log_file)
    scrapper = ImgScrapper(url, data_file, log_file, proxy_file, images_folder, result_folder, isDynamic, noisy)
    scrapper.scrape(url)
    scrapper.download()
    scrapper.zip()
    log("Status: Finishing", log_file)
    log(f"Result: ImageThief has successfully scrape {len(scrapper.getImgs())} images from {url} pages", log_file)

def downloadAllImagesFromSite(
        url: str,
        data_file: str,
        log_file: str,
        proxy_file: str,
        images_folder: str,
        result_folder: str,
        isDynamic: bool,
        noisy: bool = True,
        mode: C.ScrappingMode = C.ScrappingMode.FULL) -> None:
    log(f"Mode: Download images from whole site ({url}).", log_file)
    spider = WebCrawler(url, data_file, log_file, proxy_file, noisy)
    links_to_scrapp = spider.getAllInternalLinks()

    scrapper = ImgScrapper(url, data_file, log_file, proxy_file, images_folder, result_folder, isDynamic, noisy)
    scrapper.scrape(*links_to_scrapp)
    scrapper.download()
    scrapper.zip()
    log("Status: Finishing", log_file)
    log(f"Result: ImageThief has successfully scrape {len(scrapper.getImgs())} images from {len(links_to_scrapp)} pages", log_file)

def startProcess(request):
    user_id = request.session.session_key
    url = request.POST["url"]
    urls = extractURLs(url)
    mode = request.POST["mode"]
    log_file = request.session[f"log_file_{user_id}"]
    isDynamic = request.POST["isDynamic"]
    if isDynamic == 'true':
        isDynamic = True
        log(f"The way to parse: DYNAMIC", log_file)
    else:
        isDynamic = False
        log(f"The way to parse: STATIC", log_file)
    data_file = request.session[f"data_file_{user_id}"]
    proxy_file = request.session[f"proxy_file_{user_id}"]
    images_folder = request.session[f"image_folder_{user_id}"]
    result_folder = request.session[f"result_folder_{user_id}"]
    if mode == "full":
        mode = C.ScrappingMode.FULL
        downloadAllImagesFromSite(url, data_file, log_file, proxy_file, images_folder, result_folder, isDynamic, C.VERBOSE, mode)
    elif mode == "list-pages":
        mode = C.ScrappingMode.LIST_PAGES
        downloadAllImagesFromListPage(urls, data_file, log_file, proxy_file,  images_folder, result_folder, isDynamic, C.VERBOSE)
    else:
        mode = C.ScrappingMode.SINGLE_PAGE
        downloadAllImagesFromPage(url, data_file, log_file, proxy_file, images_folder, result_folder, isDynamic, C.VERBOSE)

def start(request):
    data = {}
    user_id = request.session.session_key
    status = 200
    request.session[f"current_log_line_{user_id}"] = 0
    startProcessProcess = Thread(target=startProcess, args=(request,))
    try:
        startProcessProcess.start()
        # Save a process pid for earlier closing (like tab, window)
        request.session[f"inWork_{user_id}"] = True
        request.session.save()
        # Max time of execution 1 hour
        startProcessProcess.join(timeout=3600)  # 1 hour
        exitCode = True
        startProcessProcess.close()
    except Exception as ex:
        exitCode = False
    else:
        exitCode = False
    imgs = os.path.join(request.session[f"result_folder_{user_id}"], "imgs.zip")
    imgs = imgs[imgs.find(os.path.join(settings.MEDIA_URL.replace('/',''),C.RESULT_FOLDER)) - 1:]
    data = {
        "btn": _("Ещё раз"),
        "imgs_path": imgs,
    }
    # If user stoped a tool, will return error code
    if exitCode:
        data["btn"] = _("Начать")
        status = 406

    return JsonResponse(data, status=status)

def init(request):
    user_id = request.session.session_key
    url = request.POST["url"]
    mode = request.POST["mode"]
    if mode == "full":
        MODE = C.ScrappingMode.FULL
    elif mode == "list-pages":
        MODE = C.ScrappingMode.LIST_PAGES
    else:
        MODE = C.ScrappingMode.SINGLE_PAGE

    proxies = []
    # If proxy file provided then convert it to python dict and put it in proxies list
    if len(request.FILES) == 1:
        proxy_file = request.FILES["proxy_file"]
        try:
            with proxy_file.open(mode='r') as file:
                proxies = json.load(file)
                if proxies[0]['weight'] != 1000:
                    proxies = []
        except:
            pass

    # If proxy genrate option provided then make a request to ProxyChecker
    proxy_generate = request.POST["proxy_generate"]
    if proxy_generate != 'EMPTY':
        if proxy_generate == 'true':
           pass # Make some request to ProxyChecker tool
        else:
            pass

    # If proxy string provided then split it an put single one proxy to proxies list
    proxy_input = request.POST["proxy_input"]
    if proxy_input != 'EMPTY':
        values = proxy_input.split(':')
        if len(values) == 3:
            protocol = proxy_input.split(':')[0]
            ip = proxy_input.split(':')[1]
            port = proxy_input.split(':')[2]
            proxies.append({
                "path": ":".join([ip,port]),
                "country": "UNKNOWN",
                "protocol": protocol,
                "type": "datacenter",
                "weight": 1000,
                "status": "unchecked"
            })
    
    
    btn = _("Ожидай")
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
    # Init proxy file
    if len(proxies) > 0:
        PROXY_FILE = os.path.join(RESULT_FOLDER, C.PROXY_FILE)
        request.session[f"proxy_file_{user_id}"] = PROXY_FILE
        removeFile(PROXY_FILE)
        initDataFile(proxies, PROXY_FILE)
    else:
        request.session[f"proxy_file_{user_id}"] = 'None'

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
