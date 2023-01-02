from django.contrib.auth.password_validation import validate_password
from django import forms
from.models import Comments,ContactModel,Users,Themes,MountainComment

class MountainCommentForm(forms.ModelForm):
    comment = forms.CharField(label="コメント", widget=forms.Textarea(attrs={
        'cols': 60,
        'rows': 5
    }))
    
    class Meta:
        model = MountainComment
        fields = ('comment',)

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }))
    email = forms.EmailField(label='メールアドレス', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter E-mail',
            'class': 'form-control',
        }))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password再入力',
        'class': 'form-control',
    }))

    class Meta:
        model = Users
        fields = ['username','email','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter E-mail',
            'class': 'form-control',
        }))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))
    remember = forms.BooleanField(label='ログイン状態を保持する',required=False)

class CreateThemeForm(forms.ModelForm):
    title = forms.CharField(label="タイトル")
    
    class Meta:
        model = Themes
        fields = ('title',)

class ThemeForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs= {
        'cols': 100,
        'rows': 5
        }))

    class Meta:
        model = Comments
        fields = ('comment',)

class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Full Name',
            'class': 'form-control',
        }))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter E-mail',
            'class': 'form-control',
        }))
    message = forms.CharField(label='お問い合わせ内容', widget=forms.Textarea(attrs={
        'placeholder': 'Enter Message',
        'class': 'form-control',
    }))

    class Meta:
        model = ContactModel
        fields = ('name','email','message',)

class DeleteThemeForm(forms.ModelForm):

    class Meta:
        model = Themes
        fields = []