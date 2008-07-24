from django.db import models

class Project(models.Model):
    """ Model for the project requests submitted on the work page
    """

    name = models.CharField(max_length = 100)
    email = models.EmailField()
    description = models.TextField()

    def __unicode__(self):
        return self.name()
