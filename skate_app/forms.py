from django import forms
from .models import Training, Schedule, Price


# Create your forms here.

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['date', 'start_time', 'end_time', 'max_students']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'start_time', 'end_time', 'price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['training_price', 'free_hour_price']
