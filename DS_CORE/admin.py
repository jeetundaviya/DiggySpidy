from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([scrapped_URL_Table,crawl_URL_Table])