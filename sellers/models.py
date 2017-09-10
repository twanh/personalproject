from django.db import models

class Seller(models.Model):
    ''' Model for sellers '''
    name        = models.CharField(max_length=50)
    search_url  = models.URLField()
    ref_url     = models.URLField(null=True, blank=True)
    logo_url    = models.URLField()
    rating      = models.CharField(max_length=5)
    desc        = models.TextField(verbose_name='Description', null=True, blank=True)

    def __str__(self):
        return self.name
