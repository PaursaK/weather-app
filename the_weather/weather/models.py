from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'