from news.models import News
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):
  fieldsets = [
	('User Info', {'fields': ['user']}),
	('title', {'fields': ['title']}),
	('message', {'fields': ['message']}),
  ]
  readonly_fields = ('user',)

admin.site.register(News, NewsAdmin)

