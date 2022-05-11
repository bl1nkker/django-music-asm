from django.contrib import admin

from music_asm.models import (
    Genre,
    Director,
    Movie,
    Ranking,
    View,
)

admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(Ranking)
admin.site.register(View)