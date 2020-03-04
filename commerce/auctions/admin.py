from django.contrib import admin

from .models import Listing, Bid, Comment, WatchlistItem

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id","creator","title","active","createdTimestamp","updatedTimestamp",)

admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(WatchlistItem)