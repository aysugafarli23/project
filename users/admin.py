from django.contrib import admin
from .models import Profile, CheckoutSessionRecord

# Register your models here.
admin.site.register(Profile)
admin.site.register(CheckoutSessionRecord)