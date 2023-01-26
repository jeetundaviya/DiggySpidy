from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator

def get_save_path(instance,filename):
    clear_url = instance.base_url.replace('.','_').replace(':','_').replace('/','_').replace('?','_').replace('+','_').replace('-','_')
    return f'{settings.DS_SAVE_SCRAPED_DATA_DIR}/{clear_url}/{filename}'

class ScrappedURL(models.Model):
    base_url = models.TextField(primary_key=True)
    last_scraped_time = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.TextField(blank=True,null=True,default=-1)
    text = models.TextField(blank=True,null=True,default=-1)
    html = models.TextField(blank=True,null=True,default=-1)
    website_category = models.CharField(max_length=50,default=-1)
    screenshot = models.ImageField(upload_to=get_save_path )
    full_screenshot = models.ImageField(upload_to=get_save_path)
    page_pdf = models.FileField(upload_to=get_save_path,validators=[FileExtensionValidator(allowed_extensions=["pdf"])])

    def __str__(self):
        return f'{self.base_url}'

class img_tag(models.Model):
    base_url = models.ForeignKey(ScrappedURL,on_delete=models.CASCADE)
    link = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','link')

    def __str__(self):
        return f"[{self.base_url}] -> {self.link}"

class a_tag(models.Model):
    base_url = models.ForeignKey(ScrappedURL,on_delete=models.CASCADE)
    link = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','link')

    def __str__(self):
        return f"[{self.base_url}] -> {self.link}"

class p_tag(models.Model):
    base_url = models.ForeignKey(ScrappedURL,on_delete=models.CASCADE)
    text = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','text')

    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h1(models.Model):
    base_url = models.ForeignKey(ScrappedURL,on_delete=models.CASCADE)
    text = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','text') 

    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h2(models.Model):
    base_url = models.ForeignKey(ScrappedURL,on_delete=models.CASCADE)
    text = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','text')

    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h3(models.Model):
    base_url = models.ForeignKey(ScrappedURL,on_delete=models.CASCADE)
    text = models.TextField(blank=True,null=True,default=-1)
    
    class Meta:
        unique_together = ('base_url','text')
    
    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h4(models.Model):
    base_url = models.ForeignKey(ScrappedURL,on_delete=models.CASCADE)
    text = models.TextField(blank=True,null=True,default=-1)
    
    class Meta:
        unique_together = ('base_url','text')  
    
    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h5(models.Model):
    base_url = models.ForeignKey(ScrappedURL,on_delete=models.CASCADE)
    text = models.TextField(blank=True,null=True,default=-1)
    
    class Meta:
        unique_together = ('base_url','text')    
    
    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h6(models.Model):
    base_url = models.ForeignKey(ScrappedURL,on_delete=models.CASCADE)
    text = models.TextField(blank=True,null=True,default=-1)
    
    class Meta:
        unique_together = ('base_url','text')
    
    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

