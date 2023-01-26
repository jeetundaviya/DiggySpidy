from django.db import models

class scrapped_URL_Table(models.Model):
    base_url = models.TextField(primary_key=True)
    url_rendered = models.BooleanField(blank=True,null=True,default=False)
    last_scraped_time = models.DateTimeField(auto_now_add=True)
    title = models.TextField(blank=True,null=True,default="NA")
    text = models.TextField(blank=True,null=True,default="NA")
    html = models.TextField(blank=True,null=True,default="NA")
    website_category = models.CharField(max_length=50,default="NA")
    screenshot = models.BinaryField(blank=True,null=True,default=b"NA")
    full_screenshot = models.BinaryField(blank=True,null=True,default=b"NA")
    page_pdf = models.BinaryField(blank=True,null=True,default=b"NA")

    def __str__(self):
        return f'{self.base_url} ({self.last_scraped_time})'

class html_Tag_Table(models.Model):
    scrapped_URL_Table = models.ForeignKey(scrapped_URL_Table,on_delete=models.CASCADE)
    tag_name = models.TextField(blank=True,null=True,default="NA")
    tag_inner_text = models.TextField(blank=True,null=True,default="NA")
    raw_tag = models.TextField(blank=True,null=True,default="NA")
    class Meta:
        unique_together = ('scrapped_URL_Table','tag_name','tag_inner_text')

    def __str__(self):
        return f"[{self.scrapped_URL_Table.base_url}] -> tag : {self.tag_name} value : {self.tag_inner_text}"

class html_Tag_Arg_Table(models.Model):
    scrapped_URL_Table = models.ForeignKey(scrapped_URL_Table,on_delete=models.CASCADE)
    html_Tag_Table = models.ForeignKey(html_Tag_Table,on_delete=models.CASCADE)
    arg_name = models.TextField(blank=True,null=True,default="NA")
    arg_value = models.TextField(blank=True,null=True,default="NA")
    class Meta:
        unique_together = ('scrapped_URL_Table','html_Tag_Table','arg_name','arg_value')

    def __str__(self):
        return f"[{self.scrapped_URL_Table.base_url}] -> tag : {self.html_Tag_Table.tag_name} -> arg_name : {self.arg_name} arg_value : {self.arg_value}"


