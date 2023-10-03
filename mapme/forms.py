from django import forms
from .models import DatabaseConfiguration

class get_kpi_form(forms.Form):
    kpi_url_field = forms.CharField(
        label="URL:",
        widget=forms.TextInput(attrs={'class': 'custom-input-class'}),
    )

class DatabaseConfigurationForm(forms.ModelForm):
    class Meta:
        model = DatabaseConfiguration
        fields = ['database_type', 'hostname', 'port', 'database_name', 'username', 'password']
        labels = {
            'hostname': 'Hostname',
            'port': 'Port',
            'database_name': 'Database Name',
            'username': 'Username',
            'password': 'Password',
        }
        widgets = {
            'database_type': forms.Select(attrs={'class': 'selection_field'}),
            'hostname': forms.TextInput(attrs={'class': 'text_field'}),
            'port': forms.NumberInput(attrs={'class': 'number_field'}),
            'database_name': forms.TextInput(attrs={'class': 'text_field'}),
            'username': forms.TextInput(attrs={'class': 'text_field'}),
            'password': forms.PasswordInput(attrs={'class': 'text_field'}),
        }