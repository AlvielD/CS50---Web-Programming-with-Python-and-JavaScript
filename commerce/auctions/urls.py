from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<uuid:id>", views.show_listing, name="listing"),
    path("bid", views.create_bid, name="bid"),
    path("categories", views.show_categories, name="categories"),
    path("watchlist", views.add_to_watchlist, name="watchlist")
]
