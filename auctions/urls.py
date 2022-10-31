from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("product_page",views.product_page,name="product_page"),
    path("comment",views.comments,name="comment"),
    path("whishlist",views.whishlist,name="whishlist"),
    path("close_bid",views.close_bid,name="close_bid"),
]
