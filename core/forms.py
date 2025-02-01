from django import forms


class PredictionForm(forms.Form):
    home_score = forms.IntegerField(
        min_value=0,
        max_value=99,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "width: 60px"}
        ),
    )
    away_score = forms.IntegerField(
        min_value=0,
        max_value=99,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "width: 60px"}
        ),
    )
