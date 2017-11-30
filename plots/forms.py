from django import forms

class plot_line_form(forms.Form):
	x_1 = forms.IntegerField(min_value = 0, max_value = 100)
	x_2 = forms.IntegerField(min_value = 0, max_value = 100)
	y_1 = forms.IntegerField(min_value = 0, max_value = 100)
	y_2 = forms.IntegerField(min_value = 0, max_value = 100)

