from django.db import models

class img_tag(models.Model):
    base_url = models.TextField()
    link = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','link')

    def __str__(self):
        return f"[{self.base_url}] -> {self.link}"

class a_tag(models.Model):
    base_url = models.TextField()
    link = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','link')

    def __str__(self):
        return f"[{self.base_url}] -> {self.link}"

class p_tag(models.Model):
    base_url = models.TextField()
    text = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','text')

    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h1(models.Model):
    base_url = models.TextField()
    text = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','text') 

    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h2(models.Model):
    base_url = models.TextField()
    text = models.TextField(blank=True,null=True,default=-1)

    class Meta:
        unique_together = ('base_url','text')

    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h3(models.Model):
    base_url = models.TextField()
    text = models.TextField(blank=True,null=True,default=-1)
    
    class Meta:
        unique_together = ('base_url','text')
    
    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h4(models.Model):
    base_url = models.TextField()
    text = models.TextField(blank=True,null=True,default=-1)
    
    class Meta:
        unique_together = ('base_url','text')  
    
    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h5(models.Model):
    base_url = models.TextField()
    text = models.TextField(blank=True,null=True,default=-1)
    
    class Meta:
        unique_together = ('base_url','text')    
    
    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class h6(models.Model):
    base_url = models.TextField()
    text = models.TextField(blank=True,null=True,default=-1)
    
    class Meta:
        unique_together = ('base_url','text')
    
    def __str__(self):
        return f"[{self.base_url}] -> {self.text}"

class heading_tags(models.Model):
    base_url = models.TextField(primary_key=True)
    h1s = models.ManyToOneRel(h1,on_delete=models.CASCADE)
    h2s = models.ManyToOneRel(h2,on_delete=models.CASCADE)
    h3s = models.ManyToOneRel(h3,on_delete=models.CASCADE)
    h4s = models.ManyToOneRel(h4,on_delete=models.CASCADE)
    h5s = models.ManyToOneRel(h5,on_delete=models.CASCADE)
    h6s = models.ManyToOneRel(h6,on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.base_url}] Headings'
    

class ParsedHTMLData(models.Model):
    base_url = models.TextField(primary_key=True)
    title = models.TextField(blank=True,null=True,default=-1)
    heading_tags = models.OneToOneField(heading_tags,on_delete=models.CASCADE)
    p_tags = models.ManyToOneRel(p_tag,on_delete=models.CASCADE)
    a_tags = models.ManyToOneRel(a_tag,on_delete=models.CASCADE)
    img_tags = models.ManyToOneRel(img_tag,on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.base_url}] -> {self.title}'

class ScrappedURL(models.Model):
    base_url = models.TextField(primary_key=True)
    last_scraped_time = models.DateTimeField(blank=True,null=True,default=-1)
    text = models.TextField(blank=True,null=True,default=-1)
    html = models.TextField(blank=True,null=True,default=-1)    
    parsed_html_content = models.OneToOneField(ParsedHTMLData,on_delete=models.CASCADE)
    website_category = models.CharField(max_length=50,default=-1)
    screenshot = models.BinaryField(blank=True,null=True,default=-1)
    full_screenshot = models.BinaryField(blank=True,null=True,default=-1)
    page_pdf = models.BinaryField(blank=True,null=True,default=-1)

    def __str__(self):
        return f'{self.base_url}'