from django import forms
from devices.models import Device


class DeviceForm(forms.ModelForm):
    # required_css_class = 'required'

    class Meta:
        model = Device
        fields = [
            'name',
            'device_type',
            'device_id',
            'lane_1',
            'lane1_name',
            'enable_1',
            'lane_2',
            'lane2_name',
            'enable_2',
            'lane_3',
            'lane3_name',
            'enable_3',
            'lane_4',
            'lane4_name',
            'enable_4',
            'lane_5',
            'lane5_name',
            'enable_5',
            'lane_6',
            'lane6_name',
            'enable_6',
            'lane_7',
            'lane7_name',
            'enable_7',
            'lane_8',
            'lane8_name',
            'enable_8',
            'description',
            'state',
            'city',
            'lat',
            'lng',
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'device_image': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id' : 'customFile',
                    'required': False,
                }
            ),
            'lane_1': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'lane1_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'enable_1': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'id': 'enable_1',
                }
            ),

            'lane_2': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'lane2_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_2': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'id': 'enable_2',
                }
            ),

            'lane_3': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'lane3_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_3': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'id': 'enable_3',
                }
            ),

            'lane_4': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lane4_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_4': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'id': 'enable_4',
                }
            ),
            'lane_5': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lane5_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_5': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'id': 'enable_5',
                }
            ),
            'lane_6': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lane6_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_6': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'id': 'enable_6',
                }
            ),
            'lane_7': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lane7_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_7': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'id': 'enable_7',
                }
            ),
            'lane_8': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'lane8_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'enable_8': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'id': 'enable_8',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                }
            ),
            'state': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'city': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'lat': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'lng': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        

            'remote_address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': False,
                }
            ),

            'enable': forms.CheckboxInput(
                attrs={
                    'class': 'form-control'
                }
            ),

        }

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control'
            if i not in ['enable']:
                self.fields[i].widget.attrs['class'] = 'form-control'
    
    def get_initial_for_field(self, field, field_name, *args, **kwargs):
        if field_name == 'description':
            return self.instance.description
        return super(DeviceForm, self).get_initial_for_field(field, field_name, *args, **kwargs)
        # return super().get_initial_for_field(field, field_name)




class DeviceField(forms.ModelForm):
    device_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))  
    class Meta:
        model = Device
        fields = ['device_images']


class DeviceLaneForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['lane_1', 'lane_2', 'lane_3', 'lane_4', 'lane_5', 'lane_6', 'lane_7', 'lane_8']