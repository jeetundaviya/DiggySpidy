from DS_Core.diggy_spidy import ds_obj
from django.shortcuts import render
import pandas as pd
import os
import mimetypes
import time 
import shutil

# Import HttpResponse module
from django.http.response import HttpResponse

from .models import ScrapingSettings

DATA_DICT = None

# Create your views here.
def home(response):
    global DATA_DICT     

    slow_mode = ScrapingSettings.objects.get(feature='slow')

    torrify = ScrapingSettings.objects.get(feature='torrify')

    if response.method == "POST":
        link = response.POST.get('link')

        do_render_html = response.POST.get('do_render_html')
        
        enable_tor_proxy = response.POST.get('enable_tor_proxy')
        
        print(f'[+] do_render_html :- {do_render_html}')

        if 'http' not in link:
            link = 'https://'+link

        ds_obj.base_url = link

        ds_obj.is_slow_mode = True if do_render_html else False

        ds_obj.must_torrify = True if enable_tor_proxy else False

        only_url = link.replace("https","").replace("http","").replace("://","")

        DATA_DICT = ds_obj.scrap(url=link)
        
        if DATA_DICT:
            
            data_dict = DATA_DICT.copy()

            slow_mode.enable = True if do_render_html else False
            slow_mode.save()

            torrify.enable = True if enable_tor_proxy else False
            torrify.save()

            if do_render_html:
                
                if data_dict["screenshot_location"] != "NA":
                    print(f'[+] Screenshot successfully found for {link}')
                    shutil.copyfile(data_dict["screenshot_location"],os.path.join("Home",os.path.join("static",os.path.join("assets","latest_ss.png"))))
                    print(f'[+] Screenshot successfully copied to latest_ss.png')
            data_dict.pop("folder_location") # Removing Folder Locatiion from the JSON Data

            excel_file_location = data_dict.pop("excel_file_location")

            excel_file_location = excel_file_location.replace('\\','\\\\')

            if os.path.isfile(excel_file_location):
                print(f'[+] location :- {excel_file_location} [Found]')
            else:
               print(f'[+] location :- {excel_file_location} [Not Found]') 
            html_table = pd.DataFrame().from_dict(data_dict,orient='index').transpose().to_html(classes='table table-striped',index=False)

            DATA_DICT = None # re-setting its value

            return render(response,"home.html",{"Data_Dictonary":data_dict,"Only_URL":only_url ,"URL":link,"Table":html_table,"Excel_File_Location":excel_file_location,"slow_mode": slow_mode.enable ,"torrify": torrify.enable})
        else:
            DATA_DICT = None # re-setting its value
            print(f'[-] Error :- {ds_obj.errors}')
            error_msg = f"Failed scrape the {link} due to {'[->]'.join(ds_obj.errors)}"
            return render(response,"home.html",{"ERROR_MSG":error_msg,"slow_mode": slow_mode.enable ,"torrify": torrify.enable})
    else:
        DATA_DICT = None # re-setting its value
        return render(response,"home.html",{"slow_mode": slow_mode.enable ,"torrify": torrify.enable})

def dashboard(response):
    return render(response,"dashboard.html",{})

def download(request):
    global DATA_DICT
    if DATA_DICT['excel_file_location'] != '':
        
        # Open the file for reading content
        path = open(DATA_DICT['excel_file_location'] , 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(DATA_DICT['excel_file_location'])
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser

        link = ds_obj.base_url

        only_url = link.replace("https","").replace("http","").replace("://","")

        response['Content-Disposition'] = "attachment; filename=%s" % only_url+".xlsx"
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'home.html')