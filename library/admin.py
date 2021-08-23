from django.contrib import admin
from .models import Client, Books, Borrow

# Register your models here.
admin.site.register(Client)
admin.site.register(Books)
admin.site.register(Borrow)
admin.site.site_header = 'Library'
admin.site.site_title = 'Library'
