# importing forms from django config directory
from django import forms
# importing user model to connect form
from models import UserModel


# signup class for getting form submitted data
class SignUpForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['name', 'username', 'email', 'password']