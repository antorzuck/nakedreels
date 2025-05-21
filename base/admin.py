
from django.contrib import admin
from .models import *


admin.site.register(Video)
admin.site.register(Category)

admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(SearchQuery)
