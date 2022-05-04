from datetime import date, datetime

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View

from main.models import Category, Institution, InstitutionCategories, Donation, DonationCategories


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
        try:
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

            checked_categories = request.POST.get('checked_categories_for_backend').split(',')
            for category_name in checked_categories:
                DonationCategories.objects.create(
                donation=donation,
                category=Category.objects.get(name=category_name)
                )

            email = request.user.email
            email_subject = f'Donation nr {donation.id}'
            email_body = f'Thank you for donating. Pick up date: {pick_up_date} at {pick_up_time}'
            send_mail(
            email_subject,
            email_body,
            'noreply@noreply.com',
            [email],
            fail_silently=False,
            )

            return render(request, 'form-confirmation.html')
        except ValueError:
            messages.error(request, 'Something went wrong')
            return redirect('/add_donation/')


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
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            donation.time_taken = current_time
            donation.save()
        else:
            donation.is_taken = False
            donation.save()
        return render(request, 'donation-details.html', {'donation': donation,
                                                         'donation_categories': donation_categories})
