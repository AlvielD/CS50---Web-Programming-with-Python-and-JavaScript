from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.render_entry, name="entry_page"),
    path("results", views.show_results, name="results"),
    path("create", views.create_newpage, name="create"),
    path("random", views.random_page, name="random")
]
