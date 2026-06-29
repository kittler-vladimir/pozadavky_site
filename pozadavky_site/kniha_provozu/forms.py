from django import forms
from .models import ZaznamKnihaProvozu


class ZaznamKnihaProvozuForm(forms.ModelForm):
    class Meta:
        model = ZaznamKnihaProvozu
        fields = [
            'den', 'cas', 'kde_server', 'dir', 'popis', 'text', 'kdo', 'poznamka',
        ]
        widgets = {
            'den': forms.DateInput(attrs={'type': 'date'}),
            'cas': forms.TimeInput(attrs={'type': 'time'}),
            'text': forms.Textarea(attrs={'rows': 5}),
            'poznamka': forms.Textarea(attrs={'rows': 3}),
        }
