from django.shortcuts import render
from django.http import JsonResponse
from .models import brand
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def getFeed(request):
    return JsonResponse({"hello": "world"})

# get default search page brands
def getSearchPageData(request):
    brand_list = []
    get_brands = brand.objects.all()[:10]
    for item in get_brands:
        brand_object = {"name":item.name, "description":item.description, "category":item.category,"logo":item.logo, "website":item.website}
        brand_list.append(brand_object)
    return JsonResponse({"data":brand_list})

# get trends

# get news

# create account
@csrf_exempt
def createAccount(request):
    post_name = request.POST.get("name")
    print(post_name)
    return JsonResponse({"data":post_name})

# delete account

# get account details

# update account

# create post

# create post catalogue

# create post product

# create post like

# delete post like

# create post view

# follow brand

# unfollow brand

# create basket

# delete basket

# share basket

# unshare basket

# send notification

# verify firebase auth
