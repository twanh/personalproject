from django.db import models

class Game(models.Model):
    ''' The Model to store games '''

    # Name of the game
    name = models.CharField(max_length=100,
                            blank=True)

    # Description of the game
    desc = models.TextField(blank=True)

    image_url = models.URLField(verbose_name='Image URL',
                                null=True,
                                blank=True)
    
    # Original Price of the game
    original_price = models.DecimalField(max_digits=6,
                                         decimal_places=2,
                                         blank=True,
                                         null=True)

    # Price on g2a
    g2a_price = models.DecimalField(max_digits=6, 
                                    decimal_places=2,
                                    blank=True, 
                                    null=True
                                    )

    # Url on g2a
    g2a_url = models.URLField(verbose_name='G2a URL',
                              null=True,
                              blank=True
                             )

    # Price on kinguin
    kinguin_price = models.DecimalField(max_digits=6, 
                                        decimal_places=2,
                                        blank=True,
                                        null=True
                                        )

    kinguin_url = models.URLField(verbose_name='Kinguin URL',
                              null=True,
                              blank=True
                             )

    # Price on greenman
    greenman_price = models.DecimalField(max_digits=6, 
                                         decimal_places=2,
                                         blank=True, 
                                         null=True
                                        )

    greenman_url = models.URLField(verbose_name='Greenman URL',
                              null=True,
                              blank=True
                             )                            

    # Price on gamestop
    gamestop_price = models.DecimalField(max_digits=6, 
                                         decimal_places=2,
                                         blank=True,
                                         null=True
                                         )

    gamestop_url = models.URLField(verbose_name='Gamestop URL',
                              null=True,
                              blank=True
                             )
                
    # Image ulrs to images for the game
    images = models.TextField(blank=True, default='[]')