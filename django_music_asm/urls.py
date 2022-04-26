from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django_music_asm import settings
from music_asm.main_views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
