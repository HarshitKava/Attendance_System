from .models import *
from django import forms

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = '__all__'
        # remove the required attribute from the fields
        widgets = {
            'Faculty_id': forms.TextInput(attrs={'required': False}),
            'Day': forms.TextInput(attrs={'required': False}),
            'Start': forms.TextInput(attrs={'required': False}),
            'End': forms.TextInput(attrs={'required': False}),
            'Subject': forms.TextInput(attrs={'required': False}),
            'RoomNo': forms.TextInput(attrs={'required': False}),
            'Code': forms.TextInput(attrs={'required': False}),
            'Batch': forms.TextInput(attrs={'required': False}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'