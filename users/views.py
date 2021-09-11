from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages

from taggit.models import Tag

from articles.models import Article
from stocksetfsbonds.models import StocksETFsBonds
from .models import AdvUser
from .forms import ChangedUserInfoForm, RegisterUserForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # context['articles_list'] = Article.objects.all()[:10]
        return context


@login_required
def profile(request):
    user_articles = Article.objects.filter(author=request.user.pk)
    bookemarked_articles = Article.objects.filter(bookmark=request.user.pk)
    tags_list = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
    securities_types_list = StocksETFsBonds.objects.all()
    context = {'user_articles': user_articles, 'tags_list': tags_list, 'securities_types_list': securities_types_list, 'bookemarked_articles': bookemarked_articles}
    return render(request, 'users/profile.html', context)

#
# class ProfileView(LoginRequiredMixin, DetailView):
#     model = AdvUser
#     template_name = 'users/profile.html'
#     # необходимо для указания адреса в шаблоне
#     slug_field = 'username'
#     # необходимо чтобы заработал маршрут в urls.py
#     slug_url_kwarg = 'username'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # 5 тегов с наиболшим количством публикаций
#         context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
#             '-articles_quantiy')[:10]
#         context['securities_types_list'] = StocksETFsBonds.objects.all()
#         # context['articles_list'] = Article.objects.all()[:10]
#         return context


class UserLogoutView(SuccessMessageMixin, LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # context['articles_list'] = Article.objects.all()[:10]
        return context


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'users/change_user_info.html'
    form_class = ChangedUserInfoForm
    success_url = reverse_lazy('users:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # context['articles_list'] = Article.objects.all()[:10]
        return context


class UserPasswordChangeVeiw(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')
    success_message = 'Пароль пользователя изменён'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # context['articles_list'] = Article.objects.all()[:10]
        return context


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = AdvUser
    template_name = 'users/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('articles:list_view')
    success_message = 'Вы успешно зарегистрировались!'

    def form_valid(self, form):
        valid = super(RegisterUserView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # context['articles_list'] = Article.objects.all()[:10]
        return context


class RegisterDoneView(TemplateView):
    template_name = 'users/register_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # context['articles_list'] = Article.objects.all()[:10]
        return context


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('articles:list_view')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # context['articles_list'] = Article.objects.all()[:10]
        return context


class ProfileView(DetailView):
    model = AdvUser
    template_name = 'users/profile_view.html'
    # необходимо для указания адреса в шаблоне
    slug_field = 'username'
    # необходимо чтобы заработал маршрут в urls.py
    slug_url_kwarg = 'username'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # context['articles_list'] = Article.objects.all()[:10]
        context['user_profile_articles'] = Article.objects.filter(author=self.object.pk, published=True)
        return context


class PrivacyView(TemplateView):
    template_name = 'users/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 5 тегов с наиболшим количством публикаций
        context['tags_list'] = Tag.objects.annotate(articles_quantiy=Count('taggit_taggeditem_items')).order_by(
            '-articles_quantiy')[:10]
        context['securities_types_list'] = StocksETFsBonds.objects.all()
        # context['articles_list'] = Article.objects.all()[:10]
        return context