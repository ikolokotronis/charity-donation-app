from django.shortcuts import render
from django.views import View
from main.models import Institution, Donation, InstitutionCategories


class LandingPageView(View):
    def get(self, request):
        supported_institutions = len(Institution.objects.all())
        donation_quantity = 0
        for donation in Donation.objects.all():
            donation_quantity += donation.quantity
        donations = len(Donation.objects.all()) + donation_quantity
        foundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        local_collections = Institution.objects.filter(type=3)
        institution_categories = InstitutionCategories.objects.all()
        return render(request, 'index.html', {'supported_institutions': supported_institutions,
                                              'donations': donations,
                                              'foundations': foundations,
                                              'organizations': organizations,
                                              'local_collections': local_collections,
                                              'institution_categories': institution_categories})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
