from django.shortcuts import render
from django.http import JsonResponse
from .models import brand, userAccount, userFollowing, post
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def getFeed(request):
    return JsonResponse({"hello": "world"})

# get default search page brands
def getSearchPageData(request):
    search_input = request.GET["searchInput"]
    user_id = request.GET["userId"]
    get_user = userAccount.objects.get(user_id=user_id)
    brand_list = []
    if request.GET['searchCategory'] != "":
        get_brands = brand.objects.filter(name__icontains=search_input,category=request.GET["searchCategory"])
    else:
        get_brands = brand.objects.filter(name__icontains=search_input)
    for item in get_brands:
        # check if user follows this brand
        user_follows = userFollowing.objects.filter(brand=item, user=get_user).exists()
        # get the brand stats
        followers_count = userFollowing.objects.filter(brand=item).count()
        post_count = post.objects.filter(brand=item).count()
        # 
        brand_object = {"id":item.id,"name":item.name, "description":item.description, "category":item.category,"logo":item.logo, "website":item.website,"following":user_follows,"post_count":post_count,"follower_count":followers_count}
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
def getAccount(request):
    user_id = request.GET["userId"]
    get_user = userAccount.objects.get(user_id=user_id)
    user_details = {"name":get_user.name,"email":get_user.email,"image":get_user.profile_image,"accept_shared_baskets":get_user.accept_shared_baskets,"mobile":get_user.mobile_number}
    return JsonResponse({"data":user_details})

# update account
@csrf_exempt
def updateAccount(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    mobile = request.POST.get("mobile")
    user_id = request.POST.get("userId")
    accept_shared_baskets = request.POST.get("accept_shared_baskets")

    get_user = userAccount.objects.get(user_id=user_id)
    get_user.name = name
    get_user.email = email
    get_user.mobile = mobile
    if accept_shared_baskets == "false":
        get_user.accept_shared_baskets = False
    else:
        get_user.accept_shared_baskets = True
    get_user.save()

    return JsonResponse({"data":"success"})

# create post

# create post catalogue

# create post product

# create post like

# delete post like

# create post view

# follow brand
def followBrand(request):
    brand_id = request.GET["id"]
    user_id = request.GET["userId"]
    get_brand = brand.objects.get(id=brand_id)
    get_user = userAccount.objects.get(user_id=user_id)
    # unfollow brand
    if userFollowing.objects.filter(brand =get_brand,user=get_user).exists():
        userFollowing.objects.filter(brand =get_brand,user=get_user).delete()
    
    # follow brand
    else:
        new_following = userFollowing()
        new_following.brand = get_brand
        new_following.user = get_user
        new_following.save()

    return JsonResponse({"data":"success"})


# get the brands that the user follows
def getFollowing(request):
    user_id = request.GET["userId"]
    get_user = userAccount.objects.get(user_id=user_id)
    brands_followed = userFollowing.objects.filter(user=get_user)
    brands_array = []
    for item in brands_followed:
        brand = item.brand
        followers_count = userFollowing.objects.filter(brand=brand).count()
        post_count = post.objects.filter(brand=brand).count()
        brand_object = {"id":brand.id,"name":brand.name, "description":brand.description, "category":brand.category,"logo":brand.logo, "website":brand.website,"following":True,"post_count":post_count,"follower_count":followers_count}
        brands_array.append(brand_object)
    return JsonResponse({"data":brands_array})


# create basket

# delete basket

# share basket

# unshare basket

# send notification

