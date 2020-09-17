from django.contrib import admin


class ArticleAdmin(admin.modelAdmin):
    list_display = ('id', 'title', 'creator', 'created', 'last_modifier', 'last_modified')
    search_fields = ('title', 'creator__username', 'content', 'id')
