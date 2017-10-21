from django.db import models

class Deal(models.Model):
    
    sellers_list = (
        ('g2a', 'G2a'),
        ('king', 'Kinguin'),
        ('gamestop', 'Gamestop')
    )

    game = models.CharField(max_length=50)
    seller = models.CharField(max_length=50,
                              choices=sellers_list)
    original_price = models.CharField(max_length=4)
    current_price = models.CharField(max_length=4)
    header_img = models.URLField()
    desc = models.TextField()

    


