from django.shortcuts import render
from django.views import View
from main.models import Institution, Donation


class LandingPageView(View):
    def get(self, request):
        supported_institutions = len(Institution.objects.all())
        donation_quantity = 0
        for donation in Donation.objects.all():
            donation_quantity += donation.quantity
        donations = len(Donation.objects.all()) + donation_quantity
        return render(request, 'index.html', {'supported_institutions': supported_institutions,
                                              'donations': donations})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
