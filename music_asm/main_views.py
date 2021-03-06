from random import randint
from django.shortcuts import render

from music_asm.models import Artist, Composition, Genre, Listening
from music_asm.utils import get_bar_plot, get_plot


def index(request):
    # generate_data()
    # drop_listenings_table()
    genre = request.GET.get('genre')
    artist = request.GET.get('artist')
    composition = request.GET.get('composition')
    context = {}
    context['labels'] = [1, 2, 3],
    context['data'] = ['Hello', 'World', 'sdgsd'],
    first_10_genres = Genre.objects.all()[:10]
    first_10_artists = Artist.objects.all()[:10]
    first_10_compositions = Composition.objects.all()[:10]
    context['genres'] = first_10_genres
    context['artists'] = first_10_artists
    context['compositions'] = first_10_compositions
    if genre or artist or composition:
        x_data = []
        y_data = []
        x_label = ''
        y_label = ''
        selected_compositions = Composition.objects.all()
        selected_compositions_and_listenings = {}
        if genre:
            genre = Genre.objects.get(genre=genre)
            selected_compositions = selected_compositions.filter(genre=genre)
            context['genre'] = genre
            listenings_by_genre = filter_listenings_by_artist_and_genre(genre)
            x_data = list(listenings_by_genre.keys())
            y_data = list(listenings_by_genre.values())
            x_label = 'Artists'
            y_label = 'Listenings'
            chart = get_bar_plot(x_data, y_data, x_label, y_label)
        if artist:
            artist = Artist.objects.get(artist=artist)
            context['artist'] = artist
            listenings_by_artist = filter_listenings_by_artist(artist)
            x_data = list(listenings_by_artist.keys())
            y_data = list(listenings_by_artist.values())
            x_label = 'Compositions'
            y_label = 'Listenings'
            chart = get_bar_plot(x_data, y_data, x_label, y_label)
            artist_compositions = Composition.objects.filter(artist=artist)
            context['artist_compositions'] = artist_compositions
        if composition:
            selected_composition = Composition.objects.get(title=composition)
            context['composition'] = composition
            listenings = Listening.objects.filter(
                composition=selected_composition, date__gte='2022-01-01')
            listenings_by_date = filter_listenings_by_date(listenings)
            x_data = list(listenings_by_date.keys())
            x_label = 'Date'
            y_data = list(listenings_by_date.values())
            y_label = 'Listenings'
            chart = get_plot(x_data, y_data, x_label, y_label)

        context['chart'] = chart
    return render(request, 'page.html', context)


def filter_listenings_by_artist_and_genre(genre):
    genre_compositions = {}
    all_artists = Artist.objects.all()
    for artist in all_artists:
        artist_compositions = Composition.objects.filter(
            artist=artist, genre=genre)
        genre_compositions[artist.artist] = len(artist_compositions)
    return genre_compositions


def filter_listenings_by_artist(artist):
    artist_compositions = Composition.objects.filter(artist=artist)
    artist_listenings = {}
    for composition in artist_compositions:
        composition_listenings = Listening.objects.filter(
            composition=composition)
        artist_listenings[composition.title] = len(composition_listenings)
    return artist_listenings


def filter_listenings_by_date(listenings):
    listenings_by_date = {}
    for listening in listenings:
        date = listening.date.strftime('%Y-%m-%d')
        if date in listenings_by_date:
            listenings_by_date[date] += 1
        else:
            listenings_by_date[date] = 1
    return listenings_by_date


def generate_data():
    all_compositions = Composition.objects.all()
    for composition in all_compositions:
        listenings_number = randint(10, 150)
        for i in range(1, listenings_number):
            Listening.objects.create(
                user='user{}'.format(i),
                composition=composition,
                date=f'2022-{randint(1,12)}-01'
            )


def drop_listenings_table():
    Listening.objects.all().delete()
