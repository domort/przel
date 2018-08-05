from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views

from backend.core import views as core_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^meal/$', core_views.MealView.as_view(), name='meal'),
    url(r'^product/list/$', core_views.ProductListView.as_view(), name='product-list'),
    url(r'^product/add/$', core_views.ProductCreateView.as_view(), name='product-add'),
    url(r'^product/(?P<slug>[-\w]+)/update$', core_views.ProductUpdateView.as_view(), name='product-edit'),

    # Customized auth / registration views
    url(r'^accounts/login/$', core_views.PrzelLoginView.as_view(), name='przel_login'),
    url(r'^accounts/register/$', core_views.PrzelRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/activate/(?P<activation_key>[-:\w]+)/$', core_views.PrzelActivationView.as_view(),
        name='registration_activate'),
    url(r'^accounts/password/reset/$', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('auth_password_reset_done'),
        html_email_template_name='registration/password_reset_email.html',
        email_template_name='registration/password_reset_email.txt'),
        name='auth_password_reset'),

    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/'
        r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('auth_password_reset_complete')
        ), name='auth_password_reset_confirm'),

    url(r'^accounts/password/reset/complete/$',
        core_views.PrzelLoginView.as_view(coming_from='auth_password_reset_complete'),
        name='auth_password_reset_complete'),

    url(r'^accounts/profile', core_views.UpdateProfileView.as_view(), name='update_profile'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'', RedirectView.as_view(url=reverse_lazy('meal')), name='home'),
]
