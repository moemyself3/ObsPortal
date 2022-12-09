from django.db import models
from django.urls import reverse

class Site(models.Model):
    name = models.CharField(max_length=20)
    geolat = models.DecimalField('Latitude in Decimal Degrees', max_digits=10, decimal_places=6)
    geolong = models.DecimalField('Longitude in Decimal Degrees', max_digits=10, decimal_places=6)
    elevation = models.DecimalField('Elevation in meters', max_digits=6, decimal_places=2)

    class Meta:
        constraints = [
                models.UniqueConstraint(fields=['name'], name='unique_site_name'),
                ]

    def get_absolute_url(self):
        return reverse('devices:site-detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name
