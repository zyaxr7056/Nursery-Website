from django import forms
from .models import ContactMessage
# from .models import UserShippingDetails


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('fullname', 'email', 'message')


# class ShippingDetailsForm(forms.ModelForm):
#     class Meta:
#         model = UserShippingDetails
#         exclude = ['user']

from .models import ProfileDetail
class ProfileDetailForm(forms.ModelForm):
    class Meta:
        model = ProfileDetail
        fields = ('name', 'email', 'contact', 'address')