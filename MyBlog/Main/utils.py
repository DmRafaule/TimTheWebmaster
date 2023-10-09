from .models import *


menu = [
    {'name': 'About', 'url_name': 'about','visible': True},
    {'name': 'Contacts', 'url_name': 'contacts','visible': True},
]

# create and fill a list with data that needed for menu
def getCategoriesMenu(toHide=None):
    ext_menu = []
    # get all available objects from database
    cat = Category.objects.all() 
    for c in cat:
        # which category will be hidden
        isVisible = True
        if c.slug == toHide:
            isVisible = False
        # append to list
        ext_menu.append({
            'name': c.name, 'url_name': c.slug,'visible': isVisible
        })
    return ext_menu
    
# define wich is gonna be visible
def getCommonMenu(toHide=None):
    for m in menu:
        isVisible = True
        if m['url_name'] == toHide:
            isVisible = False
        m['visible'] = isVisible
    return menu