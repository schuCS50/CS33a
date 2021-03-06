from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new", views.new, name="new"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("comment/<int:listing_id>", views.comment, name="comment")
]
