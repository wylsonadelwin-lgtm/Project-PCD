from django import forms
from .models import Document

class UploadFile(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('uploaded_file',)
        labels = {
            'uploaded_file': 'Pilih file untuk di unggah',
        }
        widgets = {
            'uploaded_file': forms.FileInput(attrs={
                'class':(
                    'block w-md text-sm text-gray-500 mt-2 '
                    'bg-gray-200 rounded-full shadow-[inset_0_2px_8px_rgba(0,0,0,0.6)] '
                    'file:mr-4 file:py-2 file:px-4 '
                    'file:rounded-md file:border-0 '
                    'file:text-sm file:font-semibold '
                    'file:bg-blue-50 file:text-blue-700 '
                    'hover:file:bg-blue-100'
                )
            }),
        }
