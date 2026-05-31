from django import forms
from django_flatpickr.widgets import DateTimePickerInput
from django_flatpickr.schemas import FlatpickrOptions
from.models import Poll, Question, Options, Answer
from django.forms import inlineformset_factory

class PollCreateForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'expiry']

        widgets = {
            'expiry': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            },
            format='%Y-%m-%dT%H:%M'
            )
        }

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

        widgets = {
            'text':forms.TextInput(attrs={'placeholder': 'Enter Question'})
            }

class OptionCreateForm(forms.ModelForm):
    class Meta:
        model = Options
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Enter Option'})
        }
                   


#Question Formset - tied to poll
QuestionFormSet = inlineformset_factory(
    Poll,
    Question, 
    QuestionCreateForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)

#Options Set- called per question
OptionFormSet = inlineformset_factory(
    Question,
    Options,
    OptionCreateForm,
    extra=2,
    can_delete=True,
    min_num=True,
    validate_min=True
)