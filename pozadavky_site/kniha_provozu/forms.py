from django import forms
from .models import ZaznamKnihaProvozu


class ZaznamKnihaProvozuForm(forms.ModelForm):
    class Meta:
        model = ZaznamKnihaProvozu
        fields = [
            'name', 'version', 'author', 'location', 'command',
            'type_of_launch', 'trigger_frequency', 'description',
            'link_to_details', 'status',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
