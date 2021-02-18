from django.contrib import admin
from django.urls import path
from .views import getFeed, getSearchPageData,createAccount, followBrand, getAccount, updateAccount, getFollowing,getBrandPosts
urlpatterns = [
    path('', getFeed),
    path('searchPage', getSearchPageData),
    path('createAccount', createAccount),
    path('followBrand',followBrand),
    path('getAccount',getAccount),
    path('updateAccount',updateAccount),
    path('getFollowing',getFollowing),
    path("getBrandPosts",getBrandPosts)
]