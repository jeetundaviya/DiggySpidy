from DS_Core.diggy_spidy import ds_obj
from django.shortcuts import render
import pandas as pd
import os
import mimetypes
# Import HttpResponse module
from django.http.response import HttpResponse

DATA_DICT = None

# Create your views here.
def home(response):
    global DATA_DICT     
    if response.method == "POST":

        link = response.POST.get('link')

        if 'http' not in link:
            link = 'https://'+link

        ds_obj.base_url = link

        only_url = link.replace("https","").replace("http","").replace("://","")

        DATA_DICT = ds_obj.scrap(url=link)
        
        data_dict = DATA_DICT.copy()

        if data_dict:
            
            data_dict.pop("folder_location")

            excel_file_location = data_dict.pop("excel_file_location")

            excel_file_location = excel_file_location.replace('\\','\\\\')

            if os.path.isfile(excel_file_location):
                print(f'[+] location :- {excel_file_location} [Found]')
            else:
               print(f'[+] location :- {excel_file_location} [Not Found]') 
            html_table = pd.DataFrame().from_dict(data_dict,orient='index').transpose().to_html(classes='table table-striped',index=False)

            return render(response,"home.html",{"Data_Dictonary":data_dict,"Only_URL":only_url ,"URL":link,"Table":html_table,"Excel_File_Location":excel_file_location})
        else:
            print(f'[-] Error :- {ds_obj.errors}')
            return render(response,"home.html",{"ERROR_MSG":"Failed scrape the website !"})
    else:
        return render(response,"home.html",{})

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