from django import forms

from models import TestSubject


class TestSubjectForm(forms.ModelForm):
    
    class Meta:
        model  = TestSubject
        fields = ['name', 'mail', 'gender', 'age', 'send_to']