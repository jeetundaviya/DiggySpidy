from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([ScrappedURL,ParsedHTMLData,h1,h2,h3,h4,h5,h6,heading_tags,img_tag,p_tag,a_tag])