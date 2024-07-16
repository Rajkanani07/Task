# basic URL Configurations
from django.urls import include, path

from .views import (
    ProductListView,
)

# specify URL Path for rest_framework
urlpatterns = [
    path("product_details/", ProductListView.as_view()),
]
