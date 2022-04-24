from django.contrib import admin

from music_asm.models import (
    Genre,
    Artist,
    Composition,
    Listening,

)

admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Composition)
admin.site.register(Listening)
