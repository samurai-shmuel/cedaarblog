from django.urls import path, include
from django_email_verification import urls as email_urls

from . import views
from .views import PostEdit, PostDelete

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.posts, name="posts"),
    path("posts/<int:pk>/", views.postview, name="postview"),
    path("edit/<int:pk>/", PostEdit.as_view(), name="postedit"),
    path("delete/<int:pk>/", PostDelete.as_view(), name="postdel"),
    path("delcom/<int:pk>/<int:ck>/", views.del_comment, name="commentdel"),
    path("reveal/<int:pk>/<int:ck>/", views.reveal, name="reveal"),
    path("like/<int:pk>/", views.liker, name="like_post"),
    path("posts/create/", views.postcreate, name="create"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('email/', include(email_urls)),
    path('confirm/', views.confirm, name="confirm"),
]
