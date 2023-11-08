
from django.contrib import admin
from django.urls import path, include
from . import views
from articles import urls as articles_urls
from accounts import urls as accounts_urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from articles import views as article_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', views.about),
    path('', article_views.article_list, name="home"),
    path('articles/', include(articles_urls)),
    path('accounts/', include(accounts_urls)),
    
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
