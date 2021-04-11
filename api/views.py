from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import brand, userAccount, userFollowing, post,postLike,postComment,postCatalogue,postView,postProduct,basket,basketShare
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
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

        # get the first comment if comments exist
        comments_array = []

        if post_comments_count > 0:
            first_comment = postComment.objects.filter(post=item)[:1]
            comment_data = {"user":first_comment[0].user.name,"comment":first_comment[0].comment}
            comments_array.append(comment_data)



        # get brand data
        brand = item.brand
        followers_count = userFollowing.objects.filter(brand=brand).count()
        post_count = post.objects.filter(brand=brand).count()
        brand_object = {"id":brand.id,"name":brand.name, "description":brand.description, "category":brand.category,"logo":brand.logo, "website":brand.website,"following":True,"post_count":post_count,"follower_count":followers_count}

        post_data = { "post":{"postId":item.id,"user_liked_post":user_liked_post,"post_catalogue_count":post_catalogue_count,"products_count":post_products_count,"likes_count":post_likes_count,"views_count":post_views_count,"comments_count":post_comments_count,"title":item.title,"cover":item.post_cover,"is_video":item.video,"description":item.description,"brand_id":item.brand.id,"date":item.date,"catalogue":post_catalogue},"brand":brand_object,"comments":comments_array}
        posts_array.append(post_data)

    # get trending posts
    trending_posts = getTrends(user_id)

    return JsonResponse({"data":posts_array,"trending_posts":trending_posts})

# get trends
def getTrends(userId):
    posts_array = []
    get_user = userAccount.objects.get(user_id=userId)
    trending_posts = post.objects.annotate(postLike_count=Count('postlike'))[:6]
    for item in trending_posts:
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

    return posts_array

@csrf_exempt
def addView(request):
    post_id = request.POST.get("postId")
    user_id = request.POST.get("userId")
    # 
    get_user = userAccount.objects.get(user_id=user_id)
    get_post = post.objects.get(id=post_id)

    # check if view already exists
    view_exists = postView.objects.filter(user=get_user,post=get_post).exists()
    if view_exists == False:
        new_view = postView()
        new_view.user = get_user
        new_view.post = get_post
        new_view.save()

    # get count
    view_count = postView.objects.filter(post=get_post,user=get_user).count()

    return JsonResponse({"views_count":view_count})

    


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
    push_token = request.POST.get("push_token")

    new_user = userAccount(user_id=user_id,name=name, email=email,mobile_number=mobile,push_token=push_token)
    new_user.save()
    return JsonResponse({"response":"account created"})

# delete account

# get account details
def getAccount(request):
    user_id = request.GET["userId"]
    get_user = userAccount.objects.get(user_id=user_id)
    user_details = {"name":get_user.name,"email":get_user.email,"image":str(get_user.profile_image),"accept_shared_baskets":get_user.accept_shared_baskets,"mobile":get_user.mobile_number}
    return JsonResponse({"data":user_details})

# get a user's profile using their mobile number
def getUserByNumber(request):
    user_number = request.GET["user_number"]
    does_number_exist = userAccount.objects.filter(mobile_number__icontains=user_number,accept_shared_baskets=True).exists()
    if does_number_exist == True:
        get_user = userAccount.objects.get(mobile_number__icontains=user_number)
        data = [{"profile_image":str(get_user.profile_image),"name":get_user.name,"mobile_number":get_user.mobile_number,"user_id":get_user.user_id}]
    else:
        data = []
    return JsonResponse({"data":data})

# share basket
@csrf_exempt
def shareBasket(request):
    user_id = request.POST["userId"]
    friend_id = request.POST["friendId"]
    get_user = userAccount.objects.get(user_id=user_id)
    get_friend = userAccount.objects.get(user_id=friend_id)

    # check if basket exists already
    basket_exists = basketShare.objects.filter(basket_friend=get_friend,basket_owner=get_user).exists()
    if basket_exists == True:
        share_status = "Basket already shared."
    else:
        new_basket_share = basketShare()
        new_basket_share.basket_friend = get_friend
        new_basket_share.basket_owner = get_user
        new_basket_share.viewed_by_friend = True
        new_basket_share.save()
        share_status = "Basket shared successfuly"
    
    return JsonResponse({"response":share_status})

# get a user's shared baskets 
def getSharedBaskets(request):
    user_id = request.GET["userId"]
    get_user = userAccount.objects.get(user_id=user_id)
    shared_baskets_array = []
    # get all the shared baskets related to these user
    get_baskets = basketShare.objects.filter(Q(basket_friend=get_user) | Q(basket_owner=get_user))
    for item in get_baskets:
        friend_profile_image = str(userAccount.objects.get(name=item.basket_friend).profile_image)
        data = {"friend_profile_image":friend_profile_image,"basket_friend":item.basket_friend,"owner":item.basket_owner.name,"shared_basket_id":item.id,"owner_user_id":item.basket_owner.user_id,"owner_email":item.basket_owner.email,"owner_profile_image":str(item.basket_owner.profile_image)}
        shared_baskets_array.append(data)

    return JsonResponse({"data":shared_baskets_array})

# delete shared basket
def deleteSharedBasket(request):
    shared_basket_id = request.GET["shared_basket_id"]
    get_shared_basket = basketShare.objects.get(id=shared_basket_id)
    get_shared_basket.delete()

    return JsonResponse({"response":"success"})

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


@csrf_exempt
def updateProfileImage(request):
    user_id = request.POST.get("userId")
    _file = request.FILES["profile_image"]

    get_user = userAccount.objects.get(user_id=user_id)
    get_user.profile_image = _file
    get_user.save()

    return  JsonResponse({"profile_image":str(get_user.profile_image)})


def getProfileImage(request):
    user_id = request.GET["userId"]
    get_user = userAccount.objects.get(user_id=user_id)
    return  JsonResponse({"profile_image":str(get_user.profile_image)})



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


# remove item from basket
def removeFromBasket(request):
    user_id = request.GET["userId"]
    basket_id = request.GET["basketId"]
    user_exists = userExists(user_id)

    if user_exists == True:
        get_basket = basket.objects.get(id=basket_id)
        get_basket.delete()
        return JsonResponse({"data":"success"})
    else:
        return JsonResponse({"data":"N/A"})


# get more comments
def getComments(request):
    post_id = request.GET["post_id"]
    get_post = post.objects.get(id=post_id)
    get_comments = postComment.objects.filter(post=get_post)
    comments_array = []
    for comment in get_comments:
        comment_data = {"user":comment.user.name,"comment":comment.comment}
        comments_array.append(comment_data)

    return JsonResponse({"data":comments_array})


# post comments
@csrf_exempt
def addComment(request):
    user_id = request.POST.get("userId")
    post_id = request.POST.get("postId")
    comment = request.POST.get("commentInput")

    # get post and user
    get_user = userAccount.objects.get(user_id=user_id)
    get_post = post.objects.get(id=post_id)
    # 
    new_comment = postComment()
    new_comment.user = get_user
    new_comment.post = get_post
    new_comment.comment = comment
    new_comment.save()

    # get comments
    get_comments = postComment.objects.filter(post=get_post)
    comments_array = []
    for comment in get_comments:
        comment_data = {"user":comment.user.name,"comment":comment.comment}
        comments_array.append(comment_data)

    return JsonResponse({"data":comments_array})
    







# send notification



def userExists(userId):
    user_exists = userAccount.objects.filter(user_id=userId).exists()
    return user_exists


# brands
def getWebBrandPosts(request):
    brand_id = request.GET["brandId"]
    get_brand = brand.objects.get(firebase_id=brand_id)
    # 
    get_posts = post.objects.filter(brand=get_brand)
    posts_array = []

    for item in get_posts:
        post_data = {"image":item.post_cover,"data":item.date,"title":item.title}
        posts_array.append(post_data)

    return JsonResponse({"data":posts_array})

# add new post
@csrf_exempt
def addNewPost(request):
    brand_id = request.POST.get("brandId")
    post_title = request.POST.get("postTitle")
    post_description = request.POST.get("postDescription")
    post_file = request.POST.get("postFile")
    is_video = request.POST.get("isVideo")
    # 
    get_brand = brand.objects.get(firebase_id=brand_id)

    # 
    new_post = post()
    new_post.brand = get_brand
    new_post.title = post_title
    new_post.description = post_description
    new_post.video = is_video
    new_post.post_cover = post_file
    new_post.save()

    if is_video == True:
        post_video = request.POST.get("video_location")
        new_catalogue = postCatalogue()
        new_catalogue.post = new_post
        new_catalogue.image = post_video

    return JsonResponse({"data":"uploaded"})

# add new product

# add new slide

# update account