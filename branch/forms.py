from . models import User
from django.forms import ModelForm


class CreationForm(ModelForm):
    class Meta:
        model=User
        fields=['username','email']
