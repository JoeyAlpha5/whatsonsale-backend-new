
from django.contrib import admin
from .models import userAccount,basketShare,postProduct, brand, userFollowing,basket, postCatalogue,postLike, postView, newsPost,post, postComment
# Register your models here.

class brandAdmin(admin.ModelAdmin):
    list_display = ['name','category']
    ordering = ['name']

class productAdmin(admin.ModelAdmin):
    list_display = ['name','price', 'post']


class postAdmin(admin.ModelAdmin):
    list_display = ['title','brand',"active"]

class userAccountAdmin(admin.ModelAdmin):
    list_display = ['name','mobile_number','accept_shared_baskets']

class basketShareAdmin(admin.ModelAdmin):
    list_display = ['basket_owner','basket_friend', 'viewed_by_friend']

class newsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']

class followAdmin(admin.ModelAdmin):
    list_display = ['user','brand', 'date']

class viewAdmin(admin.ModelAdmin):
    list_display = ['user','post', 'date']

class likeAdmin(admin.ModelAdmin):
    list_display = ['user','post', 'date']

class commentAdmin(admin.ModelAdmin):
    list_display = ['user','post', 'date']

admin.site.register(userAccount, userAccountAdmin)
admin.site.register(newsPost,newsPostAdmin)
admin.site.register(postProduct, productAdmin)
admin.site.register(post, postAdmin)
admin.site.register(userFollowing,followAdmin)
admin.site.register(brand, brandAdmin)
admin.site.register(postLike,likeAdmin)
admin.site.register(postView,viewAdmin)
admin.site.register(postComment,commentAdmin)
admin.site.register(postCatalogue)
admin.site.register(basket)
admin.site.register(basketShare, basketShareAdmin)