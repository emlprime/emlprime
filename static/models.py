from django.db import models
from django.template.defaultfilters import slugify

class Project(models.Model):
    """ Model for the project requests submitted on the work page
    """

    name = models.CharField(max_length = 100)
    email = models.EmailField()
    description = models.TextField()

    def __unicode__(self):
        return self.name()

class Blog(models.Model):
    """Model for the blog entry that will be displayed on the blog page of the play section
    """
    title = models.CharField(max_length = 255)
    date = models.DateField()
    entry = models.TextField()
    image_1 = models.ImageField(upload_to="images", null=True, blank=True)
    image_2 = models.ImageField(upload_to="images", null=True, blank=True)

    def __unicode__(self):
        return str(self.date)

class Comic(models.Model):
    """Model for the comics  that will be displayed on the comic page of the play section
    """
    title = models.CharField(max_length = 255)
    comic = models.ImageField(upload_to="images")
    date = models.DateField()

    class Meta:
        get_latest_by = "date"

    def __unicode__(self):
        return str(self.date)


