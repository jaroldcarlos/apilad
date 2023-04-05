from django.urls import path
from .views import PostDetail, PostList

app_name = 'blog'

urlpatterns = [
    path('tag/<slug:tag_slug>', PostList.as_view(), name='post_list_by_tag'),
    path('author/<slug:author_slug>', PostList.as_view(), name='post_list_by_author'),
    path('<slug:category_slug>/', PostList.as_view(), name='post_list_by_category'),
    path('<slug:slug>.html', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
]
