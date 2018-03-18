from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views, get_user_model
from django import forms
from products.models import Comment


class CommentForm(forms.ModelForm):
    Review = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', "placeholder": "Your review"}))
    Rate = forms.IntegerField(min_value=0, max_value=5)
    class Meta:
        model = Comment
        fields = ('Review' , 'Rate',)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Your username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Your password"}))


User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Your username"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Your password"}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email
