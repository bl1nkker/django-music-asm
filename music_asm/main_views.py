from django.shortcuts import render

from music_asm.models import Artist, Composition, Genre


def index(request):
    genre = request.GET.get('genre')
    artist = request.GET.get('artist')
    composition = request.GET.get('composition')
    print('genre:', genre)
    print('artist:', artist)
    print('composition:', composition)
    context = {}
    first_10_genres = Genre.objects.all()[:10]
    first_10_artists = Artist.objects.all()[:10]
    first_10_compositions = Composition.objects.all()[:10]
    context['genres'] = first_10_genres
    context['artists'] = first_10_artists
    context['compositions'] = first_10_compositions
    if genre or artist or composition:
        selected_compositions = Composition.objects.all()
        if genre:
            genre = Genre.objects.get(genre=genre)
            selected_compositions = selected_compositions.filter(genre=genre)
            context['genre'] = genre
        if artist:
            artist = Artist.objects.get(artist=artist)
            selected_compositions = selected_compositions.filter(artist=artist)
            context['artist'] = artist
        if composition:
            selected_compositions = selected_compositions.filter(
                title=composition)
            context['composition'] = composition
        context['selected_compositions'] = selected_compositions
    return render(request, 'page.html', context)
