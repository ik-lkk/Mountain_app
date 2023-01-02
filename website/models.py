from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,AbstractBaseUser,PermissionsMixin
)
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import datetime
# Create your models here.


class MountainManager(models.Manager):
    #山の詳細を取り出す
    def fetch_mountain(self, pk):
        return self.filter(pk=pk).first()

class Mountain(models.Model):
    name = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)
    picture = models.FileField(upload_to='mountain_pictures')

    objects = MountainManager()

    class Meta:
        db_table = 'mountain'



class MountainCommentManager(models.Manager):
    #その山の全てのコメントを取り出す
    def fetch_mountain_all(self, pk):
        return self.filter(mountain_id=pk).all()    

class MountainComment(models.Model):
    user = models.ForeignKey(
        'Users', on_delete=models.CASCADE
    )
    mountain = models.ForeignKey(
        'Mountain',on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=1000)
    create_at = models.DateTimeField(
        default=timezone.datetime.now)
    
    objects = MountainCommentManager()



class UserManager(BaseUserManager):
    #Userを作った後ログイン状態でテーマの作成や書き込みの反映をする
    def create_user(self,username,email,password=None):
        if not email:
            raise ValueError('Enter Email')
        if not username:
            raise ValueError('Enter Email')
        user = self.model(
            username =username,
            email = email
        )#userにself(Userモデル)の中身を入れた値を渡す
        user.set_password(password)
        user.save(using = self.db)
        return user

    def create_superuser(self, username,email, password=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(
        max_length=150, unique=True, verbose_name='名前')
    email = models.EmailField(max_length=255,unique=True,verbose_name='メールアドレス')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('website:home')

    class Meta:
        db_table = 'users'
        verbose_name = 'ユーザ'

class UserActivateTokensManager(models.Manager):

    

    def activate_user_by_token(self,token):
        user_activate_token = self.filter(
            token = token,
            expired_at__gte=datetime.now()).first()
        user = user_activate_token.user
        user.is_active = True
        user.save()

class UserActivateTokens(models.Model):

    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(
        'Users',on_delete=models.CASCADE
    )

    objects = UserActivateTokensManager()

    
    class Meta:
        db_table = 'user_activate_tokens'


class ThemesManager(models.Manager):
    #テーマの詳細
    def fetch_title(self,pk):
        return self.filter(pk=pk).first()



class Themes(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        'Users',on_delete=models.CASCADE
    )

    objects = ThemesManager()
    class Meta:
        db_table = 'themes'

class CommentsManager(models.Manager):
    def fetch_by_theme(self,theme_id):
        return self.filter(theme_id=theme_id).all()
    def fetch_by_first(self,theme_id):
        return self.filter(theme_id=theme_id).first()


class Comments(models.Model):

    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'Users',on_delete=models.CASCADE
    )
    theme = models.ForeignKey(
        'Themes',on_delete=models.CASCADE
    )
    create_at = models.DateTimeField(
        default=timezone.datetime.now)
    comment_order = models.IntegerField()

    objects = CommentsManager()

    class Meta:
        db_table = 'comments'

class ContactModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField(max_length=1000)

    class Meta:
        db_table = 'contact'


