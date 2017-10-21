from django.db import models

class Deal(models.Model):
    
    sellers_list = (
        ('g2a', 'G2a'),
        ('king', 'Kinguin'),
        ('gamestop', 'Gamestop')
    )

    game = models.CharField(max_length=50,
                            null=True,
                            blank=True)
    seller = models.CharField(max_length=50,
                              choices=sellers_list,
                              null=True,
                              blank=True)
    original_price = models.CharField(max_length=4,
                                    null=True,
                                    blank=True)
    current_price = models.CharField(max_length=4,
                                        null = True,
                                        blank=True)
    header_img = models.URLField(
                            null=True,
                            blank=True
    )
    desc = models.TextField(
        null=True,
        blank=True
    )

    


