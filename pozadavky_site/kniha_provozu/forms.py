from django import forms
from .models import ZaznamKnihaProvozu


class ZaznamKnihaProvozuForm(forms.ModelForm):
    launched_at = forms.DateTimeField(
        label='Spuštěno',
        required=False,
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'
        ),
    )

    class Meta:
        model = ZaznamKnihaProvozu
        fields = [
            'name', 'version', 'author', 'location', 'command', 'launched_at',
            'type_of_launch', 'trigger_frequency', 'description',
            'link_to_details', 'status',
        ]
        widgets = {
            'command': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
