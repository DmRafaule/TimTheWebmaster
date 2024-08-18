# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/t/timachuduk/timthewebmaster.com/MyBlog')
#sys.path.insert(1, '/home/t/timachuduk/timthewebmaster.com/.venv/lib/python3.11/site-packages')
sys.path.insert(1, '/home/t/timachuduk/timthewebmaster.com/venv_new/lib/python3.11/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'MyBlog.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
