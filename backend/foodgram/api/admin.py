from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Cart, Favorite, Ingredient,Recipe, Subscriptions, Tag, User


class IngredientAmountInline(admin.TabularInline):
    model = Ingredient.recipes.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    list_filter = ['measurement_unit']
    search_fields = ['name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    list_filter = ['name', 'author', 'tag']
    search_fields = ['name']
    inlines = [IngredientAmountInline]

    def in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscriber']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']
    list_filter = ['user']
    search_fields = ['user__username', 'recipe__name']