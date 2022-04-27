from django.shortcuts import render

from music_asm.models import Artist, Composition, Genre, Listening
from music_asm.utils import get_plot


def index(request):
    genre = request.GET.get('genre')
    artist = request.GET.get('artist')
    composition = request.GET.get('composition')
    print('genre:', genre)
    print('artist:', artist)
    print('composition:', composition)
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
        if artist:
            artist = Artist.objects.get(artist=artist)
            selected_compositions = selected_compositions.filter(artist=artist)
            context['artist'] = artist
        if composition:
            selected_composition = Composition.objects.get(title=composition)
            context['composition'] = composition

            listenings = Listening.objects.filter(
                composition=selected_composition)
            listenings_by_date = filter_listenings_by_date(listenings)
            x_data = list(listenings_by_date.keys())
            x_label = 'Date'
            y_data = list(listenings_by_date.values())
            y_label = 'Listenings'

        chart = get_plot(x_data, y_data, x_label, y_label)
        context['chart'] = chart
    return render(request, 'page.html', context)


def filter_listenings_by_date(listenings):
    listenings_by_date = {}
    for listening in listenings:
        print(listening)
        date = listening.date.strftime('%Y-%m-%d')
        if date in listenings_by_date:
            listenings_by_date[date] += 1
        else:
            listenings_by_date[date] = 1
    return listenings_by_date
