from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre


class Director(models.Model):
    director = models.CharField(max_length=50)

    def __str__(self):
        return self.director


class Movie(models.Model):
    title = models.CharField(max_length=50)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Ranking(models.Model):
    user = models.CharField(max_length=50)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class View(models.Model):
    user = models.CharField(max_length=50)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user