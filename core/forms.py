from django import forms
from .models import Sporcu

class SporcuForm(forms.ModelForm):
    class Meta:
        model = Sporcu
        fields = ['isim', 'kulup', 'mevki', 'boy', 'smac_yuksekligi', 'blok_yuksekligi', 'profil_fotografi', 'video_linki']
        widgets = {
            'isim': forms.TextInput(attrs={'class': 'w-full border p-2 rounded'}),
            'kulup': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
            'mevki': forms.Select(attrs={'class': 'w-full border p-2 rounded'}),
            'boy': forms.NumberInput(attrs={'class': 'w-full border p-2 rounded'}),
            'smac_yuksekligi': forms.NumberInput(attrs={'class': 'w-full border p-2 rounded'}),
            'blok_yuksekligi': forms.NumberInput(attrs={'class': 'w-full border p-2 rounded'}),
            'video_linki': forms.URLInput(attrs={'class': 'w-full border p-2 rounded', 'placeholder': 'https://youtube.com/...'}),
        }
