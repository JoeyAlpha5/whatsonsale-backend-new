from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import brand, userAccount, userFollowing, post,postLike,postComment,postCatalogue,postView,postProduct,basket
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def getFeed(request):
    user_id = request.GET["userId"]
    feed_count = int(request.GET["feedCount"])
    get_user = userAccount.objects.get(user_id=user_id)
    brands_followed = userFollowing.objects.filter(user=get_user)
    followed_brands = []
    posts_array = []
    # push array of followed brands
    for following in brands_followed:
        followed_brands.append(following.brand)
    # get posts of brands that are in followed list
    posts = post.objects.filter(brand__in=followed_brands).order_by('-id')[feed_count:feed_count+5]
    for item in posts:
        # check if the user has liked the post
        user_liked_post = postLike.objects.filter(user=get_user,post=item).exists()
        # check if the user has viewed the post
        post_likes_count = postLike.objects.filter(post=item).count()
        post_views_count = postView.objects.filter(post=item).count()
        post_comments_count = postComment.objects.filter(post=item).count()
        post_products_count = postProduct.objects.filter(post=item).count()
        post_catalogue_count = postCatalogue.objects.filter(post=item).count()
        # if count is more than 1
        if post_catalogue_count > 0:
            # get all the catalogues for the slide
            post_catalogue = serialize("json", postCatalogue.objects.filter(post=item))
        else:
            post_catalogue = []

        # get brand data
        brand = item.brand
        followers_count = userFollowing.objects.filter(brand=brand).count()
        post_count = post.objects.filter(brand=brand).count()
        brand_object = {"id":brand.id,"name":brand.name, "description":brand.description, "category":brand.category,"logo":brand.logo, "website":brand.website,"following":True,"post_count":post_count,"follower_count":followers_count}

        post_data = { "post":{"postId":item.id,"user_liked_post":user_liked_post,"post_catalogue_count":post_catalogue_count,"products_count":post_products_count,"likes_count":post_likes_count,"views_count":post_views_count,"comments_count":post_comments_count,"title":item.title,"cover":item.post_cover,"is_video":item.video,"description":item.description,"brand_id":item.brand.id,"date":item.date,"catalogue":post_catalogue},"brand":brand_object}
        posts_array.append(post_data)

    return JsonResponse({"data":posts_array})

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

# get brand post gallery 
def getBrandPosts(request):
    brand_id = request.GET["brandId"]
    user_id = request.GET["userId"]
    get_brand = brand.objects.get(id=brand_id)
    get_posts = post.objects.filter(brand=get_brand)
    get_user = userAccount.objects.get(user_id=user_id)
    posts_array = []
    for item in get_posts:
        # check if the user has liked the post
        user_liked_post = postLike.objects.filter(user=get_user,post=item).exists()
        # check if the user has viewed the post
        post_likes_count = postLike.objects.filter(post=item).count()
        post_views_count = postView.objects.filter(post=item).count()
        post_comments_count = postComment.objects.filter(post=item).count()
        post_products_count = postProduct.objects.filter(post=item).count()
        post_catalogue_count = postCatalogue.objects.filter(post=item).count()
        # if count is more than 1
        if post_catalogue_count > 0:
            # get all the catalogues for the slide
            post_catalogue = serialize("json", postCatalogue.objects.filter(post=item))
        else:
            post_catalogue = []
    
        post_data = {"postId":item.id,"user_liked_post":user_liked_post,"post_catalogue_count":post_catalogue_count,"products_count":post_products_count,"likes_count":post_likes_count,"views_count":post_views_count,"comments_count":post_comments_count,"title":item.title,"cover":item.post_cover,"is_video":item.video,"description":item.description,"brand_id":brand_id,"date":item.date,"catalogue":post_catalogue}
        posts_array.append(post_data)

    return JsonResponse({"data":posts_array})

#  create post

# create post catalogue

# create post product

# create post like
@csrf_exempt
def Like(request):
    user_id = request.POST.get("userId")
    post_id = request.POST.get("postId")
    get_post = post.objects.get(id=post_id)
    get_user = userAccount.objects.get(user_id=user_id)
    user_liked_post = postLike.objects.filter(user=get_user,post=get_post).exists()
    if user_liked_post == True:
        postLike.objects.filter(user=get_user,post=get_post).delete()
    else:
        new_post_like = postLike()
        new_post_like.user = get_user
        new_post_like.post = get_post
        new_post_like.save()

    return JsonResponse({"data":"success"})


# delete post like

# create post view

# follow brand
def followBrand(request):
    brand_id = request.GET["id"]
    user_id = request.GET["userId"]
    get_brand = brand.objects.get(id=brand_id)
    get_user = userAccount.objects.get(user_id=user_id)
    # unfollow brand
    if userFollowing.objects.filter(brand=get_brand,user=get_user).exists():
        userFollowing.objects.filter(brand=get_brand,user=get_user).delete()
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



# get post products
def getPostProducts(request):
    post_id = request.GET["postId"]
    userId = request.GET["userId"]
    # check if user exists
    user_exists = userExists(userId)

    if user_exists == True:
        get_post = post.objects.get(id=post_id)
        get_products = serialize("json",postProduct.objects.filter(post=get_post))
        return JsonResponse({"data":get_products})
    else:
        return JsonResponse({"data":"N/A"})


# add to basket
@csrf_exempt
def addToBasket(request):
    user_id = request.POST.get("userId")
    product_id = request.POST.get("productId")
    get_user = userAccount.objects.get(user_id=user_id)
    get_product = postProduct.objects.get(id=product_id)

    # product exists in basket
    product_exists_in_basket = basket.objects.filter(user=get_user,product=get_product).exists()

    if product_exists_in_basket == True:
        return JsonResponse({"data":"Product already in basket"})
    else:
        new_product_in_basket = basket()
        new_product_in_basket.user = get_user
        new_product_in_basket.product =get_product
        new_product_in_basket.save()
        return JsonResponse({"data":"Product added in basket"})

# get basket
def getBasket(request):
    user_id = request.GET["userId"]
    get_user = userAccount.objects.get(user_id=user_id)
    get_basket = basket.objects.filter(user=get_user)
    products_array = []
    for item in get_basket:
        data = {"id":item.id,"name": item.product.name,"price":item.product.price,"image":item.product.image,"brand_logo":item.product.post.brand.logo}
        products_array.append(data)
    return JsonResponse({"data":products_array})

# share basket

# unshare basket

# send notification



def userExists(userId):
    user_exists = userAccount.objects.filter(user_id=userId).exists()
    return user_exists