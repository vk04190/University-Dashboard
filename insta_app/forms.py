# importing forms from django config directory
from django import forms
# importing user model to connect form
from models import UserModel,PostModel


# signup class for getting form submitted data
class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['name', 'username', 'email', 'password']


# signin class for validating userid and password
class SignInForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'password']


# post form controller
class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image', 'caption']