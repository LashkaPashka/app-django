from django.shortcuts import HttpResponseRedirect
from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse, reverse_lazy

from user.models import User
from coom.views import TitleMixin

from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView

from django.contrib.messages.views import SuccessMessageMixin
from user.models import Verification_Email


class UserLoginViews(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm


class RegistrationViews(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    title = 'Регистрация'
    form_class = UserRegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = ('Вы зарегистрированы!')


class EmailVerificationViews(TemplateView):
    template_name = 'user/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = self.kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = Verification_Email.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verification = True
            user.save()
            return super(EmailVerificationViews, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))



class ProfileUpdateViews(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    title = 'Store - Личный кабинет'
    template_name = 'user/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))









'''@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
        'baskets': Baskets.objects.filter(user=request.user),
    }
    return render(request, 'user/profile.html', context)
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
    
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'user/login.html', context)
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы зарегистрированы!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'user/registration.html', context)'''
