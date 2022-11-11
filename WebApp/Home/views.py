from DS_Core.diggy_spidy import ds_obj
from django.shortcuts import render
import json

# Create your views here.
def home(response):
    
    if response.method == "POST":

        link = response.POST.get('link')

        if 'http' not in link:
            link = 'https://'+link

        ds_obj.base_url = link

        data_dict = ds_obj.scrap(url=link)
        
        data_dict.pop("folder_location")
        
        return render(response,"home.html",{"JSON_Output":data_dict,"URL":link})
    else:
        return render(response,"home.html",{})

def dashboard(response):
    return render(response,"dashboard.html",{})
    