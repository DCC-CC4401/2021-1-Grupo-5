from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        error_messages = {
            'username': {
                'required': 'Your Custom Error Message here !!!',
            },
        }
        labels = {'email':'Email'}
