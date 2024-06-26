from django import forms
from ckeditor.widgets import CKEditorWidget
from classroom.models import Course


class NewCourseForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), max_length=40, required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'validate'}), required=True)
    syllabus = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Course
        fields = ('picture', 'title', 'description', 'syllabus')
