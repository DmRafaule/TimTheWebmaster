def getSlugFromURL(url: str) -> str:
    url_elements_clean = []
    for el in url.split('/'):
        if len(el) > 0:
            url_elements_clean.append(el)
    return url_elements_clean[2]