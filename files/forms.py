from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .models import UserInput


class FileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, file):
        if file.size > self.max_size:
            raise ValidationError(f"File size should be less than {self.max_size} bytes.")

class UserInputForm(forms.ModelForm):
    file = forms.FileField(label='File',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            FileSizeValidator(max_size=1024 * 1024)  # Maximum file size: 1MB
        ],
        required=False
    )
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        
        # Check if a file with the same name already exists
        if file:
            existing_user_input = UserInput.objects.filter(file__iexact=file.name).exists()
            if existing_user_input:
                self.add_error('file', 'A file with the same name already exists.')
        
        return cleaned_data
    class Meta:
        model = UserInput
        fields = ['email', 'address', 'phone', 'file']

