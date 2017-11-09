# importing forms from django config directory
from django import forms
# importing user model to connect form
from models import UserModel, PostModel, LikeModel, CommentModel


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


# Like form data pass
class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = ['post']


#  Comment form Pass Data From here
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['comment_text', 'post']