from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import views as auth_views
from django.http import Http404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView,View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,FormView
from .models import Mountain,Themes,Comments,Users,UserActivateTokens
from .forms import ThemeForm,ContactForm,UserLoginForm,RegistForm,MountainCommentForm,MountainComment,DeleteThemeForm
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate,login,logout
from .import forms
from django.db import transaction
from django.contrib import messages

from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class RegistView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('website:regist_success')

class RegistSuccess(TemplateView):
    template_name = 'regist_success.html'


#is_activeの条件をつけなくてもFalseだと失敗する
class UserLoginView(FormView):
    template_name = 'user_login.html'
    form_class = UserLoginForm
    def post(self,request,*args, **kwargs):
        form = forms.UserLoginForm(request.POST or None)
        if form.is_valid():
            remember = form.cleaned_data['remember']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #ユーザがログイン状態を保持する場合
            if remember:
                self.request.session.set_expiry(1200000)
            username = Users.objects.filter(email = email).first()
            user = authenticate(username = username,email=email,password=password)

            if user:
                if user.is_active:#ユーザのメール認証が済んでいるか
                    login(request,user)
                    return redirect('website:home')
                else:
                    #print(user.is_active)
                    messages.error(request, 'ユーザの本登録がされていません。メールをご確認ください')
                    return redirect('website:user_login')
            else:
                messages.error(request,'メールアドレスかパスワードが間違っています。')
                return redirect('website:user_login')
        else:
            messages.error(request, '入力が間違っています。今一度確認をお願いします。')
            return redirect('website:user_login')

class UserLogoutView(LogoutView):
    pass


class MountainListView(ListView):
    model = Mountain
    template_name = 'mountain_list.html'

    def get_queryset(self):#山の名前で検索する
        query = super().get_queryset()
        mountain_name = self.request.GET.get('mountain_name')
        if mountain_name:
            query = query.filter(
                name =mountain_name
            )
        return query

class MountainDetailView(View):
    template_name = 'mountain_detail.html'
    def get(self, request, pk,*args, **kwargs):
        form = forms.MountainCommentForm()
        #山の詳細とそれに紐づくコメントを全て取り出す
        mountain = Mountain.objects.fetch_mountain(pk)
        mountain_comment = MountainComment.objects.fetch_mountain_all(pk)

        return render(request, 'mountain_detail.html', context={
            'form': form,
            'mountain':mountain,
            'mountain_comment':mountain_comment
        })

    @transaction.atomic
    def post(self, request, pk, *args, **kwargs):
        form = forms.MountainCommentForm(request.POST or None)
        mountain = Mountain.objects.fetch_mountain(pk)
        mountain_comment = MountainComment.objects.fetch_mountain_all(pk)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.mountain_id = mountain.id
            form.save()
        return render(request, 'mountain_detail.html', context={
            'form': form,
            'mountain': mountain,
            'mountain_comment': mountain_comment
        })


class ThemeListView(ListView):
    template_name = 'theme_list.html'

    def get(self, request, *args, **kwargs):
        #全てのテーマ、テーマ作成フォーム,それに紐づくコメント、全てのコメントを取得
        themes = Themes.objects.all()
        form = forms.CreateThemeForm()
        commentx = forms.ThemeForm()
        first_comment = Comments.objects.all()
        return render(request, 'theme_list.html', context={
            'form': form,
            'themes': themes,
            'commentx':commentx,
            'first_comment':first_comment,
        })
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = forms.CreateThemeForm(request.POST or None)
        commentx = forms.ThemeForm(request.POST or None)
        themes = Themes.objects.all()
        first_comment = Comments.objects.all()
        if form.is_valid() and commentx.is_valid():
            form.instance.user = request.user
            form.save()
            comments = form.save(commit=False)
            commentx.instance.user = request.user
            commentx.instance.theme_id = comments.id
            commentx.instance.comment_order = 1
            commentx.save()
    
        return render(request, 'theme_list.html', context={
            'form': form,
            'themes': themes,
            'commentx':commentx,
            'first_comment':first_comment,
        })

class ThemeDetail(View):
    template_name = 'theme_detail.html'

    def get(self,request,theme_id,*args, **kwargs):
        #テーマのタイトルとそのコメント全て取り出す
        theme = Themes.objects.fetch_title(theme_id)
        comments = Comments.objects.fetch_by_theme(theme_id)
        form = forms.ThemeForm()
        return render(request, 'theme_detail.html', context={
            'form':form,
            'comments':comments,
            'theme':theme
        })

    def post(self,request,theme_id,*args, **kwargs):
        form = forms.ThemeForm(request.POST or None)
        theme = Themes.objects.fetch_title(theme_id)
        comments = Comments.objects.fetch_by_theme(theme_id)
        last_comment = Comments.objects.filter(theme_id=theme_id).last()
        last_comment_id = last_comment.comment_order+1
        if form.is_valid():
            form.instance.theme_id = theme.id
            form.instance.user = request.user
            form.instance.comment_order = last_comment_id
            form.save()
        return render(request, 'theme_detail.html', context={
            'form':form,
            'comments':comments,
            'theme':theme
        })

class Contact(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('website:contact_success')

    def form_valid(self,form):
        if form.is_valid():
            form.save()
        return super(Contact,self).form_valid(form)

class ContactSuccess(TemplateView):
    template_name = 'contact_success.html'



#メールにアクセスしたユーザを有効化(signals.pyと合わせて)
def activate_user(request,token):
    user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
    return render(
        request,'activate_user.html'
    )

#タイトルを更新（作成者のみ）
def edit_theme(request,id):
    theme = get_object_or_404(Themes,id=id)
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(request.POST or None,instance=theme)
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        return redirect('website:theme_list')
    return render(
        request,'edit_theme.html',context = {
            'edit_theme_form':edit_theme_form,
            'id':id
        }
    )

#テーマごと削除(作成者のみ)
def delete_theme(request,id):
    theme = get_object_or_404(Themes,id=id)
    if theme.user.id != request.user.id:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    if delete_theme_form.is_valid():
        theme.delete()
        return redirect('website:theme_list')
    return render(request,'delete_theme.html',context = {
        'delete_theme_form':delete_theme_form
    })

