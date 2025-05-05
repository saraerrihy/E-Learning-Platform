from django import forms
from .models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time_limit', 'required_score_to_pass']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class QuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'style': 'border: 1px solid #0d6efd;',
            'placeholder': 'Enter your True/False question here...'
        }),
        required=True
    )
    
    points = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control bg-dark text-white',
            'style': 'border: 1px solid #0d6efd;',
            'min': '1',
            'value': '1'
        }),
        initial=1,
        min_value=1
    )
    
    correct_answer = forms.ChoiceField(
        choices=[('true', 'True'), ('false', 'False')],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input bg-dark'
        }),
        required=True
    )

    class Meta:
        model = Question
        fields = ['question_text', 'points']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.question_type = 'true-false'
        if commit:
            instance.save()
            
            # Create True and False answers
            Answer.objects.create(
                question=instance,
                answer_text='True',
                is_correct=self.cleaned_data['correct_answer'] == 'true'
            )
            Answer.objects.create(
                question=instance,
                answer_text='False',
                is_correct=self.cleaned_data['correct_answer'] == 'false'
            )
            
        return instance

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'is_correct']

AnswerFormSet = forms.inlineformset_factory(
    Question,
    Answer,
    form=AnswerForm,
    extra=2,
    min_num=2,
    max_num=2,
    validate_min=True,
    can_delete=False
) 