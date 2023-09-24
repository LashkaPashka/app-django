from django.contrib import admin
from user.models import User, Verification_Email

admin.site.register(User)
admin.site.register(Verification_Email)