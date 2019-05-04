from django.contrib import admin
from django.urls import path, include

auth_urls = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]

api_urls = [
    path('auth/', include(auth_urls)),
    path('', include('publication.api.urls')),
    path('', include('account.api.urls')),
    path('', include('feed.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
]
