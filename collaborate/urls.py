from django.contrib import admin
from django.urls import path, include

auth_urls = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]

api_urls = [
    path('auth/', include(auth_urls)),
    path('', include('publications.api.urls')),
    path('', include('accounts.api.urls')),
    path('', include('feed.api.urls')),
    path('', include('bookmarks.api.urls')),
    path('', include('preferences.api.urls')),
    path('', include('votes.api.urls')),
    path('', include('tags.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
