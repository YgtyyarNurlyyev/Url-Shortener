import uuid

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from main.models import Url


# Create your views here.
@login_required
def index(request):
    short_link = ''

    if request.method == 'POST':
        link = request.POST['link']
        uid = str(uuid.uuid4())[:5]
        short_url = Url(link=link, short_link=uid, author=request.user)
        short_link = 'http://localhost:8000/' + uid
        short_url.save()

    context = {
        'short_link': short_link,
    }

    return render(request, 'index.html', context)


def redirect_url(request, link):
    try:
        url_object = Url.objects.get(short_link=link)
        return redirect(url_object.link)
    except:
        raise Http404("Poll does not exist")


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


class Register(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)


class HistoryList(LoginRequiredMixin, ListView):
    model = Url
    context_object_name = 'urls'
    template_name = 'history.html'

    def get_queryset(self):
        new_context = Url.objects.filter(
            author=self.request.user,
        )

        return new_context
