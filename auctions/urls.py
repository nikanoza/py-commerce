from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("filter", views.filter_categories, name="filter"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove/<int:id>", views.remove_from_listing, name="remove"),
    path("add/<int:id>", views.add_to_watchlist, name="add"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:id>", views.add_comment, name="comment"),
    path("bid/<int:id>", views.make_bid, name="bid")
]
