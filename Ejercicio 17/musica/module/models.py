from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=100)
    picture_url = models.URLField(max_length=100)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    value = models.CharField(max_length=50)

class ArtistUser(models.Model):
    user_id = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    listen_time = models.IntegerField()

class ArtistUserTag(models.Model):
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    