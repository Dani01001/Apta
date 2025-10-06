from django import forms
from .models import Reserva, Restaurante

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre', 'telefono', 'fecha', 'hora', 'restaurante']

    restaurante = forms.ModelChoiceField(
        queryset=Restaurante.objects.all(),
        widget=forms.Select(attrs={'readonly': 'readonly'}),
        empty_label=None  # Esto evita que haya una opción vacía
    )
