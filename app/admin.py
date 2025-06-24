from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Favourite

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'user', 'types', 'height', 'weight', 'base_experience')
    search_fields = ('name', 'types', 'user__username')
    list_filter = ('types',)

