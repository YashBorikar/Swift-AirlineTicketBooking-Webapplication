from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class BookingForm(forms.Form):
    OPTIONS = (
        ('Mr.','Mr.'),
        ('Mrs.','Mrs.'),
        ('Ms.','Ms.'),
    )

    Title = forms.ChoiceField(choices=OPTIONS)
    First_Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Traveller First Name'}))
    Second_Name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Traveller Second Name'}))
    Email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address: name@example.com'}))
    Contact_Number = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Contact Number'}))
    Address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'House/ Building Name, Street/Road Name, Locality Name'}))
    City = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    State = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'State'}))
    Zip_Code = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Zip-Code'}))

    bot_handler=forms.CharField(required=False, widget=forms.HiddenInput)

    def clean(self):
        cleaned_data=super().clean()

        bot_handler_value = cleaned_data['bot_handler']
        fname = cleaned_data['First_Name']
        sname = cleaned_data['Second_Name']
        number = cleaned_data['Contact_Number']
        city = cleaned_data['City']
        state = cleaned_data['State']

        if len(bot_handler_value)>0:
            raise forms.ValidationError("Form is accessed by BOT, unable to process form!")

        if fname.isalpha() and sname.isalpha():
            pass
        else: raise forms.ValidationError("Enter Valid Name")

        if city:
            if city.isalpha():
                pass
            else: raise forms.ValidationError("Enter Valid City")

        if state:
            if state.isalpha():
                pass
            else: raise forms.ValidationError("Enter Valid State")

        if len(str(number))!=10:
            raise forms.ValidationError("Please Enter Valid Contact Number")
