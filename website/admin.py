from django.contrib import admin
from .models import Mountain, Themes, Comments, Users, ContactModel
# Register your models here.

admin.site.register(Mountain)
admin.site.register(Users)
admin.site.register(Comments)
admin.site.register(Themes)
admin.site.register(ContactModel)






