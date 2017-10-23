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

    buy_url = models.URLField(
        null=True,
        blank=True
    )

    desc = models.TextField(
        null=True,
        blank=True
    )


    def __str__(self):
        return self.game
    
    
    def get_ref_url(self):
        if self.buy_url:
            if self.seller == 'king':
                return ''.join([self.buy_url, '?r=42864'])
            else:
                return self.buy_url
        else:
            return ''