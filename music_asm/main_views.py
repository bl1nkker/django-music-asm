from random import randint
from django.shortcuts import render

from music_asm.models import Director, Movie, Genre, Ranking, View
from music_asm.utils import get_bar_plot, get_plot


def index(request):
    # generate_data()
    # drop_listenings_table()
    # generate_movies()
    genre = request.GET.get('genre')
    director = request.GET.get('director')
    movie = request.GET.get('movie')
    context = {}
    context['labels'] = [1, 2, 3],
    context['data'] = ['Hello', 'World', 'sdgsd'],
    first_10_genres = Genre.objects.all()[:10]
    first_10_directors = Director.objects.all()[:10]
    first_10_movies = Movie.objects.all()[:10]
    context['genres'] = first_10_genres
    context['directors'] = first_10_directors
    context['movies'] = first_10_movies
    if genre or director or movie:
        x_data = []
        y_data = []
        x_label = ''
        y_label = ''
        selected_compositions = Movie.objects.all()
        selected_compositions_and_listenings = {}
        if genre:
            genre = Genre.objects.get(genre=genre)
            selected_compositions = selected_compositions.filter(genre=genre)
            context['genre'] = genre
            listenings_by_genre = filter_listenings_by_artist_and_genre(genre)
            x_data = list(listenings_by_genre.keys())
            y_data = list(listenings_by_genre.values())
            x_label = 'Director'
            y_label = 'Views'
            chart = get_bar_plot(x_data, y_data, x_label, y_label)
            # Sort movies by genre
            movies_by_genre = Movie.objects.filter(genre=genre)
            print('Movies by genre:', movies_by_genre)
            # [{}, {}, {}]
            top_5_movies = filter_ranking_by_movies(movies_by_genre)
            x_2_data = list(top_5_movies.keys())
            y_2_data = list(top_5_movies.values())
            x_2_label = 'Movie'
            y_2_label = 'Rank'
            chart2 = get_bar_plot(x_2_data, y_2_data, x_2_label, y_2_label)
            context['chart2'] = chart2
        if director:
            director = Director.objects.get(director=director)
            context['director'] = director
            listenings_by_artist = filter_listenings_by_artist(director)
            x_data = list(listenings_by_artist.keys())
            y_data = list(listenings_by_artist.values())
            x_label = 'Movies'
            y_label = 'Views'
            chart = get_bar_plot(x_data, y_data, x_label, y_label)
            artist_compositions = Movie.objects.filter(director=director)
            context['artist_compositions'] = artist_compositions
        if movie:
            selected_composition = Movie.objects.get(title=movie)
            context['movie'] = movie
            listenings = Ranking.objects.filter(
                movie=selected_composition, date__gte='2022-01-01')
            listenings_by_date = filter_listenings_by_date(listenings)
            x_data = list(listenings_by_date.keys())
            x_label = 'Date'
            y_data = list(listenings_by_date.values())
            y_label = 'Views'
            chart = get_plot(x_data, y_data, x_label, y_label)

        context['chart'] = chart
    return render(request, 'page.html', context)


def filter_listenings_by_artist_and_genre(genre):
    genre_compositions = {}
    all_artists = Director.objects.all()
    for director in all_artists:
        artist_compositions = Movie.objects.filter(
            director=director, genre=genre)
        genre_compositions[director.director] = len(artist_compositions)
    return genre_compositions


def filter_listenings_by_artist(director):
    director_movies = Movie.objects.filter(director=director)
    director_views = {}
    for movie in director_movies:
        movie_views = View.objects.filter(
            movie=movie)
        director_views[movie.title] = len(movie_views)
    return director_views


def filter_listenings_by_date(listenings):
    listenings_by_date = {}
    for listening in listenings:
        date = listening.date.strftime('%Y-%m-%d')
        if date in listenings_by_date:
            listenings_by_date[date] += 1
        else:
            listenings_by_date[date] = 1
    return listenings_by_date


def filter_ranking_by_movies(movies):
    all_rankings = Ranking.objects.all()
    ranking_by_movies = {}
    for ranking in all_rankings:
        if ranking.movie in movies:
            if ranking.movie.title in ranking_by_movies:
                ranking_by_movies[ranking.movie.title].append(ranking)
            else:
                ranking_by_movies[ranking.movie.title] = [ranking]
    for movie, rankings in ranking_by_movies.items():
        # [Rank, Rank, Rank]
        ranking_by_movies[movie] = sum(
            [ranking.score for ranking in rankings]) / len(rankings)
    # { 'The Batman': 3,5, 'The Joker': 4,5, 'The Dark Knight': 0 }
    top_5_movies = dict(
        # (movie, score)
        sorted(ranking_by_movies.items(), key=lambda item: item[1])[:5])
    return top_5_movies


def generate_data():
    all_compositions = Movie.objects.all()
    for movie in all_compositions:
        listenings_number = randint(10, 150)
        ranking_number = randint(10, 150)
        for i in range(1, listenings_number):
            View.objects.create(
                user='user{}'.format(i),
                movie=movie,
                date=f'2022-{randint(1,12)}-01'
            )
        for i in range(1, ranking_number):
            Ranking.objects.create(
                user='user{}'.format(i),
                movie=movie,
                date=f'2022-{randint(1,12)}-01',
                score=randint(0, 10)
            )


def drop_listenings_table():
    Ranking.objects.all().delete()
    View.objects.all().delete()


def generate_movies():
    movies = ['The Shawshank Redemption', 'The Godfather', 'The Godfather II', 'The Dark Knight', 'The Green Mile', '12 Angry',
              'Schindler\'s List', 'Pulp Fiction',
              'The Lord of the Rings: The Two Towers', 'The Lord of the Rings: The Return of the King',
              'Fight Club', 'The Matrix', 'Inception', 'The Lord of the Rings: The Fellowship of the Ring', 'The Batman Begins',
              'The Dark Knight Rises', 'The Hobbit: An Uftherlands Tale', 'The Hobbit: The Desolation of Smaug',
              'The Hobbit: The Battle of the Five Armies', 'The Hobbit: The Desolation of Smaug', 'The Hobbit: The Battle of the Five Armies',
              'Memento', 'The Prestige', 'Die Hard']
    all_directors = Director.objects.all()
    all_genres = Genre.objects.all()

    for movie in movies:
        director = all_directors[randint(0, len(all_directors) - 1)]
        genre = all_genres[randint(0, len(all_genres) - 1)]
        Movie.objects.create(
            title=movie,
            director=director,
            genre=genre
        )
