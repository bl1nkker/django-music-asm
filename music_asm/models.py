from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre


class Artist(models.Model):
    artist = models.CharField(max_length=50)

    def __str__(self):
        return self.artist


class Composition(models.Model):
    title = models.CharField(max_length=50)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Listening(models.Model):
    user = models.CharField(max_length=50)
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user
