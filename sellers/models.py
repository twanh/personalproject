from django.db import models

class Seller(models.Model):
    ''' Model for sellers '''
    name = models.CharField(max_length=50)
    search_url = models.URLField()
    logo_url = models.URLField()
    rating = models.CharField(max_lenght=5)

    def __str__(self):
        return self.name
