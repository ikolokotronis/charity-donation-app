from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.views import View
from main.models import Institution, Donation, InstitutionCategories
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail


class LandingPageView(View):
    def get(self, request):
        supported_institutions = len(Institution.objects.all())
        bag_quantity = 0
        for donation in Donation.objects.all():
            bag_quantity += donation.quantity
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
                                              'bag_quantity': bag_quantity,
                                              'foundations': foundations,
                                              'organizations': organizations,
                                              'local_collections': local_collections,
                                              'institution_categories': institution_categories})

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        message = request.POST.get('message')
        email_subject = f'Contact form (Sent by user {name} {surname}'
        email_body = message
        administrators = User.objects.filter(is_superuser=True)

        if not name or not surname or not message:
            messages.error(request, 'Please fill all fields correctly')
            return redirect('/')

        for administrator in administrators:
            email = administrator.email
            send_mail(
                email_subject,
                email_body,
                'noreply@noreply.com',
                [email],
                fail_silently=False,
            )
        messages.success(request, 'Successfully sent')
        return redirect('/')
