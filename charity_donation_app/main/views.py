import datetime
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.views import View
from main.models import Institution, Donation, InstitutionCategories, Category, DonationCategories
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import date


class LandingPageView(View):
    def get(self, request):
        supported_institutions = len(Institution.objects.all())
        donation_extra_quantity = 0
        for donation in Donation.objects.all():
            donation_extra_quantity += donation.quantity
        donation_quantity = len(Donation.objects.all()) + donation_extra_quantity
        foundation_list = Institution.objects.filter(type=1)
        organization_list = Institution.objects.filter(type=2)
        local_collection_list = Institution.objects.filter(type=3)
        foundation_paginator = Paginator(foundation_list, 5)
        organization_paginator = Paginator(organization_list, 5)
        local_collection_paginator = Paginator(local_collection_list, 5)
        page_num = request.GET.get('page', 1)
        try:
            foundations = foundation_paginator.page(page_num)
        except EmptyPage:
            foundations = foundation_paginator.page(1)
        try:
            organizations = organization_paginator.page(page_num)
        except EmptyPage:
            organizations = organization_paginator.page(1)
        try:
            local_collections = local_collection_paginator.page(page_num)
        except EmptyPage:
            local_collections = local_collection_paginator.page(1)
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


class DonationDetailsView(View):
    def get(self, request, donation_id):
        donation = Donation.objects.get(id=donation_id)
        donation_categories = DonationCategories.objects.all()
        return render(request, 'donation-details.html', {'donation': donation,
                                                         'donation_categories': donation_categories})

    def post(self, request, donation_id):
        donation = Donation.objects.get(id=donation_id)
        donation_categories = DonationCategories.objects.all()
        is_taken = request.POST.get('is_taken')
        if is_taken == "true":
            donation.is_taken = True
            donation.date_taken = date.today()
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            donation.time_taken = current_time
            donation.save()
        else:
            donation.is_taken = False
            donation.save()
        return render(request, 'donation-details.html', {'donation': donation,
                                                         'donation_categories': donation_categories})


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
        donations = Donation.objects.filter(user_id=user_id).order_by('date_added')\
            .order_by('date_taken').order_by('time_taken').order_by('is_taken')
        donation_categories = DonationCategories.objects.all()
        return render(request, 'user_panel.html', {'donations': donations,
                                                   'donation_categories': donation_categories})


class UserEditView(View):
    def get(self, request, user_id):
        if request.user.id != user_id:
            return redirect(f'/edit/{request.user.id}/')
        return render(request, 'user-edit.html')

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        if not request.POST.get('password') or not request.POST.get('password2'):
            return render(request, 'user-edit.html', {'error_text': 'Uzupełnij pola'})
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            return render(request, 'user-edit.html', {'error_text': 'Hasła różnią się od siebie'})
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return render(request, 'user-edit.html', {'success_text': 'Dane zostały zmienione'})


class PasswordChangeView(View):
    def get(self, request, user_id):
        if request.user.id != user_id:
            return redirect(f'/edit/{request.user.id}/')
        return render(request, 'change-password.html')

    def post(self, request, user_id):
        if not request.POST.get('old_password') or not request.POST.get('new_password1') \
                or not request.POST.get('new_password2'):
            return render(request, 'change-password.html', {'error_text': 'Uzupełnij pola'})

        old_password = request.POST.get('old_password')
        user = authenticate(request, username=request.user.email, password=old_password)
        if user is None:
            return render(request, 'change-password.html', {'error_text': 'Stare hasło niepoprawne'})

        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if new_password1 != new_password2:
            return render(request, 'change-password.html', {'error_text': 'Hasła różnią się od siebie'})

        user.set_password(new_password1)
        user.save()
        return render(request, 'change-password.html', {'success_text': 'Dane zostały zmienione'})
