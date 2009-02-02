from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.syndication.feeds import Feed


OWNER_CHOICES = (
    ('P', 'Peter'),
    ('L', 'Laura')
)

class Portfolio(models.Model):
    """ Model for the portfolio objects listed on the peter and laura profile pages
    """
    
    owner = models.CharField(choices=OWNER_CHOICES, max_length=5)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images", null=True, blank=True)

    def __unicode__(self):
        return self.url

class Project(models.Model):
    """ Model for the project requests submitted on the work page
    """

    name = models.CharField(max_length = 100)
    email = models.EmailField()
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Blog(models.Model):
    """Model for the blog entry that will be displayed on the blog page of the play section
    """
    title = models.CharField(max_length = 255)
    date = models.DateField()
    entry = models.TextField()
    image_1 = models.ImageField(upload_to="images", null=True, blank=True)
    image_2 = models.ImageField(upload_to="images", null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return str(self.date)

class Comic(models.Model):
    """Model for the comics  that will be displayed on the comic page of the play section
    """
    title = models.CharField(max_length = 255)
    comic = models.ImageField(upload_to="images/comics")
    date = models.DateField()

    class Meta:
        get_latest_by = "date"

    def __unicode__(self):
        return str(self.date)


class BlogFeed(Feed):
    """ Model for submitting the latest blog entries to the RSS feed
    """

    title = "EML' Blog"
    link = "/play/blog/"
    description = "EML' official blog.  Accept no substitutes."
    copyright = "Copyright (c) 2009, EMLPrime"

    def author_name(self):
        return "Peter Stradinger"

    def author_email(self):
        return "peter@emlprime.com"

    def copyright(self):
        return copyright

    def item_link(self):
        return "http://www.emlprime.com/play/blog/"

    def items(self):
        return Blog.objects.order_by('-date')[:10]

class ComicFeed(Feed):
    """ Model for submitting the latests comics to the RSS feed
    """

    title = "Boobies!"
    link = "/play/comic/"
    description = "A comic by EML'.  We all think these things, but are too embarassed to admit it."
    copyright = "Copyright (c) 2009, EMLPrime"

    def author_name(self):
        return "Peter Stradinger"

    def author_email(self):
        return "peter@emlprime.com"

    def copyright(self):
        return copyright

    def item_link(self):
        return "http://www.emlprime.com/play/comic/"

    def items(self):
        return Comic.objects.order_by('-date')[:10]
