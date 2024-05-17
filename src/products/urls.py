from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.ProductsView.as_view(), name="list"),
    path("carts/", views.CartsView.as_view(), name="carts"),
    path("carts/<str:slug>/add/", views.CartAddView.as_view(), name="cart-add"),
    path(
        "carts/<str:slug>/remove/", views.CartRemoveView.as_view(), name="cart-remove"
    ),
    path(
        "carts/<str:slug>/delete/", views.CartDeleteView.as_view(), name="cart-delete"
    ),
    path(
        "carts/<str:slug>/checked/",
        views.CartCheckedView.as_view(),
        name="cart-checked",
    ),
    path("<str:slug>/", views.ProductView.as_view(), name="detail"),
]
