"""charity_donation_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import LandingPageView, AddDonationView, LoginView, RegisterView, \
    LogoutView, UserPanelView, DonationDetailsView, UserEditView, PasswordChangeView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view()),
    path('add_donation/', AddDonationView.as_view(), name='donation-page'),
    path('donation/<int:donation_id>/', DonationDetailsView.as_view()),
    path('login/', LoginView.as_view(), name='login-page'),
    path('register/', RegisterView.as_view(), name='registration-page'),
    path('logout/', LogoutView.as_view(), name='logout-page'),
    path('panel/<int:user_id>/', UserPanelView.as_view(), name='panel-page'),
    path('edit/<int:user_id>/', UserEditView.as_view(), name='user-edit-page'),
    path('change_password/<int:user_id>/', PasswordChangeView.as_view())
]
