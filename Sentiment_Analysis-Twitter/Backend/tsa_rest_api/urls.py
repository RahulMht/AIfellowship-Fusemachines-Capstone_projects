from django.urls import re_path
from tsa_rest_api import views

urlpatterns = [
    re_path('classified-tweets', views.index),
    re_path('classified-tweets/<int:id>', views.index),
    re_path('train-classifier', views.train_classifier),
    re_path('fetch-tweets', views.classify_tweets),
]
