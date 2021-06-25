from django.db import models
from account.models import BloggerAccount
from ckeditor.fields import RichTextField

def get_uplaod_file_name(userpic, filename,):
    return u'blog/%s/%s%s' % (str(userpic.blogger_id)+"/blogimages","",filename)

class Blogs(models.Model):
    blogger = models.ForeignKey(BloggerAccount, on_delete=models.DO_NOTHING)
    pub_date = models.DateField(null=True, blank=True, )
    image = models.ImageField(upload_to= get_uplaod_file_name, null=True, blank=True,)
    content = RichTextField(null=True, blank=True,)
    title = models.CharField(max_length=100)