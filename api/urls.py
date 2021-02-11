from django.contrib import admin
from django.urls import path
from .views import getFeed, getSearchPageData,createAccount
urlpatterns = [
    path('', getFeed),
    path('searchPage', getSearchPageData),
    path('createAccount', createAccount)
]