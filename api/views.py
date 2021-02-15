from django.shortcuts import render
from django.http import JsonResponse
from .models import brand, userAccount
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def getFeed(request):
    return JsonResponse({"hello": "world"})

# get default search page brands
def getSearchPageData(request):
    search_input = request.GET["searchInput"]
    brand_list = []
    if request.GET['searchCategory'] != "":
        get_brands = brand.objects.filter(name__icontains=search_input,category=request.GET["searchCategory"])
    else:
        get_brands = brand.objects.filter(name__icontains=search_input)
    for item in get_brands:
        brand_object = {"id":item.id,"name":item.name, "description":item.description, "category":item.category,"logo":item.logo, "website":item.website}
        brand_list.append(brand_object)
    return JsonResponse({"data":brand_list})


# get trends

# get news

# create account
@csrf_exempt
def createAccount(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    mobile = request.POST.get("mobile")
    user_id = request.POST.get("user_id")

    new_user = userAccount(user_id=user_id,name=name, email=email,mobile_number=mobile)
    new_user.save()
    return JsonResponse({"response":"account created"})

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
