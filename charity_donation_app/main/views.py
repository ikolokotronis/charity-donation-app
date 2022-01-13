from django.shortcuts import render, redirect
from django.views import View
from main.models import Institution, Donation, InstitutionCategories, Category, DonationCategories
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class LandingPageView(View):
    def get(self, request):
        supported_institutions = len(Institution.objects.all())
        donation_extra_quantity = 0
        for donation in Donation.objects.all():
            donation_extra_quantity += donation.quantity
        donation_quantity = len(Donation.objects.all()) + donation_extra_quantity
        foundations = Institution.objects.filter(type=1)
        organizations = Institution.objects.filter(type=2)
        local_collections = Institution.objects.filter(type=3)
        institution_categories = InstitutionCategories.objects.all()
        return render(request, 'index.html', {'supported_institutions': supported_institutions,
                                              'donation_quantity': donation_quantity,
                                              'foundations': foundations,
                                              'organizations': organizations,
                                              'local_collections': local_collections,
                                              'institution_categories': institution_categories})


class AddDonationView(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        institution_categories = InstitutionCategories.objects.all()
        return render(request, 'form.html', {'categories': categories,
                                             'institutions': institutions,
                                             'institution_categories': institution_categories})

    def post(self, request):
        quantity = request.POST.get('bags')
        institution = Institution.objects.get(name=request.POST.get('organization'))
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        phone_number = request.POST.get('phone')
        pick_up_date = request.POST.get('date')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = request.user
        donation = Donation.objects.create(
            quantity=quantity,
            institution=institution,
            address=address,
            city=city,
            zip_code=zip_code,
            phone_number=phone_number,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user
        )

        checked_categories = request.POST.get('checked_categories_backend').split(',')
        for category in checked_categories:
            DonationCategories.objects.create(
                donation=donation,
                category=Category.objects.get(name=category)
            )

        return render(request, 'form-confirmation.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/register')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            User.objects.create_user(username=email, first_name=name, last_name=surname, email=email, password=password)
            return redirect('/login')
        elif password != password2:
            return render(request, 'register.html', {'error_text': 'Hasła nie pasują do siebie!'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class UserPanelView(View):
    def get(self, request, user_id):
        donations = Donation.objects.filter(user_id=user_id)
        donation_categories = DonationCategories.objects.all()
        return render(request, 'user_panel.html', {'donations': donations,
                                                   'donation_categories': donation_categories})
