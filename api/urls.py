from django.contrib import admin
from django.urls import path
from .views import getFeed,Like ,getSearchPageData,createAccount, followBrand, getAccount, updateAccount, getFollowing,getBrandPosts,getPostProducts,addToBasket,getBasket,removeFromBasket,updateProfileImage,getProfileImage
urlpatterns = [
    path('getFeed', getFeed),
    path('searchPage', getSearchPageData),
    path('createAccount', createAccount),
    path('followBrand',followBrand),
    path('getAccount',getAccount),
    path('updateAccount',updateAccount),
    path('getFollowing',getFollowing),
    path("getBrandPosts",getBrandPosts),
    path("postLike",Like),
    path("getPostProducts",getPostProducts),
    path("addToBasket",addToBasket),
    path("getBasket",getBasket),
    path("removeFromBasket",removeFromBasket),
    path("updateProfileImage",updateProfileImage),
    path("getProfileImage",getProfileImage),
]