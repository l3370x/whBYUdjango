from request.models import Request
from django.contrib import admin

class RequestAdmin(admin.ModelAdmin):
  fieldsets = [
	('User name', {'fields': ['fk_student']}),
	('Team name', {'fields': ['fk_team']}),
  ]
  readonly_fields = ('fk_student','fk_team',)

admin.site.register(Request, RequestAdmin)