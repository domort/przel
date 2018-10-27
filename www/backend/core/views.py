import urllib
import urllib2
import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.forms import ValidationError
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string

from registration.backends.hmac.views import RegistrationView, ActivationView
from backend.core.models import Product
from backend.core.forms import EmailBasedUserForm
from backend.core.models import EmailBasedUser, Meal


class MealView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'meal.html'

    def get_context_data(self, **kwargs):
        try:
            meal = self.request.user.meal
        except Meal.DoesNotExist:
            meal = None
        return {'user_meal': meal}

    def post(self, request, *args, **kwargs):
        pass


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    model = Product
    template_name = 'product/product_form.html'
    fields = ['name', 'unit_weight', 'unit_description', 'category', 'protein', 'carb', 'fat', 'energy', 'fat_sat',
              'fiber', 'salt']


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Product
    slug_url_kwarg = 'slug'
    template_name = 'product/product_form.html'
    fields = ['name', 'unit_weight', 'unit_description', 'category', 'protein', 'carb', 'fat', 'energy', 'fat_sat',
              'fiber', 'salt']


class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    template_name = 'product/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context.update({"title": "Product List"})
        # context.update({'object_list': models.Product.objects.all().extra(select={'lower_name': 'lower(name)'}).order_by('lower_name')})
        return context


class PrzelLoginView(auth_views.LoginView):
    coming_from = None

    def get(self, request, *args, **kwargs):
        if self.coming_from in ['auth_password_reset_complete', ]:
            messages.success(request, 'Your password has been reset successfully!')
        return super(PrzelLoginView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(PrzelLoginView, self).get_initial()
        try:
            email = self.request.GET.get('email')
        except:
            email = None

        if email:
            try:
                validate_email(email)
            except ValidationError as e:
                pass
            else:
                initial['username'] = email
        return initial


class PrzelRegistrationView(RegistrationView):
    form_class = EmailBasedUserForm
    email_body_template_txt = 'registration/activation_email.txt'
    email_body_template_html = 'registration/activation_email.html'

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({'user': user})
        subject = render_to_string(self.email_subject_template, context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(self.email_body_template_txt, context)
        html_msg = render_to_string(self.email_body_template_html, context)
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL, html_message=html_msg)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        try:
            result = json.load(response)
        except:
            result = {}
        recaptcha_succeded = result.get('success', False)
        if not recaptcha_succeded:
            form.add_error('recaptcha', "Invalid reCAPTCHA. Please confirm that you are a human.")

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PrzelActivationView(ActivationView):
    success_msg = 'Your account has been activated successfully. You can now login.'

    def get_success_url(self, activated_user=None):
        success_url = reverse('auth_login')
        if activated_user:
            success_url = '{}?email={}'.format(success_url, activated_user.email)
        return success_url

    def activate(self, *args, **kwargs):
        activated = super(PrzelActivationView, self).activate(*args, **kwargs)
        if activated:
            storage = messages.get_messages(self.request)
            for _ in storage:
                pass
            messages.success(self.request, self.success_msg)
        return activated


class UpdateProfileView(LoginRequiredMixin, generic.UpdateView):
    model = EmailBasedUser
    fields = ['first_name', 'last_name']
    template_name = 'registration/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user
