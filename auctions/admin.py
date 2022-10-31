from django.contrib import admin

from auctions.views import whishlist
from .models import autionlisting,categorylist,User, comment,wishlists
# Register your models here.
admin.site.register(autionlisting)
admin.site.register(categorylist)
admin.site.register(User)
admin.site.register(comment)
admin.site.register(wishlists)

