from django import forms
# from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm

from devices.models import Device
from .models import UserDevices, UserProfile
import logging

User = get_user_model()

logger = logging.getLogger(__name__)

class LoggingMixin(object):
    def add_error(self, field, error):
        if field:
            logger.info('Form error on field %s: %s', field, error)
        else:
            logger.info('Form error: %s', error)
        super().add_error(field, error)

class UserAdminCreationForm(forms.ModelForm, LoggingMixin):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['email', 'full_name', ]

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email','full_name', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]










class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))

    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Fullname",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))


    class Meta:
        model = User
        fields = ('email','full_name',  'password1', 'password2',)




    def clean_password(self):
        '''
        Verify both passwords match.
        '''
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

 
class CreateUsers(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    

    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Fullname",
                "class": "form-control"
            }
        ))

    org = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Organisation",
                "class": "form-control"
            }
    ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))
    
    # admin = forms.BooleanField(
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             "placeholder": "Admin",
    #             "class": "form-control"
    #         }
    #     ))
    
    # staff = forms.BooleanField(
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             "placeholder": "Staff",
    #             "class": "form-control"
    #         }
    #     ))
    
    # normal_user = forms.BooleanField(
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             "placeholder": "Normal User",
    #             "class": "form-control"
    #         }
    #     ))
    
    # advanced_user = forms.BooleanField(
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             "placeholder": "Advanced User",
    #             "class": "form-control"
    #         }
    #     ))

#     


    class Meta:
        model = User
        fields = ('email','full_name',  'password1', 'password2', 'admin', 'staff', 'normal_user', 'advanced_user', 'org')



class UpdateUser(UserAdminChangeForm):
    class Meta:
        model = User
        fields = '__all__'




    def clean_password(self):
        '''
        Verify both passwords match.
        '''
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CreateUsers, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CreateUserDevice(forms.ModelForm):
    
    class Meta:
        model = UserDevices
        fields = [
            'user_detail',
            'device_name', 
            'active',          
        ]
        

        widgets = {
            'user_detail': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'device_name': forms.Select(
                
                attrs={
                    "class": "form-control"
                }
            ),

            'active': forms.CheckboxInput(
                attrs={
                    "class": "form-control"
                }
            ),

        
        }


# class UserDeviceImage(forms.ModelForm):
#     device_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))  
#     class Meta:
#         model = UserDevices
#         fields = ['device_images']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'full_name']
    
class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'photo',
            'bio',
            'address',
            'city',
            'state',
            'zip_code',
            'country',
            'phone_number',
            'website',
            'facebook',
            'twitter',
            'instagram',
            'youtube',
            'linkedin',
            'github',
            'google_plus',
            'pinterest',
            'tumblr',
            'vimeo',
            'flickr',
            'dribbble',
            'behance',
            'reddit',
        ]


        widgets = {
            'username': forms.TextInput(
                attrs={
                    "class": "form-control"

                }
            ),
            'email': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'photo': forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'bio': forms.Textarea(
                attrs={
                    "class": "form-control"
                }
            ),

            'address': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'city': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'state': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'zip_code': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'country': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'phone_number': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'website': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'facebook': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'twitter': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'instagram': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'youtube': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'linkedin': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'github': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'google_plus': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'pinterest': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'tumblr': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'vimeo': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'flickr': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'dribbble': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'behance': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            'reddit': forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),


        }


