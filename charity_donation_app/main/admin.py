from django.contrib import admin
from main.models import Category, Institution, Donation, InstitutionCategories, DonationCategories

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
admin.site.register(InstitutionCategories)
admin.site.register(DonationCategories)