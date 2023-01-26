"""site_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from blog.views import homepage, posts, post, category_view, like_view, AddCommentView, SearchResultsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('posts', posts, name='posts'),
    path('post/<int:pk>/', post, name='post'),
    path('category/<str:category>/', category_view, name='category'),
    path('like/<int:pk>', like_view, name='like_post'),
    path('post/<int:pk>/comment', AddCommentView.as_view(), name='add_comment'),
    path("search/", SearchResultsView.as_view(), name="search_results"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
