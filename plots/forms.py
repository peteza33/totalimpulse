from django import forms

class plot_line_form(forms.Form):
	x_1 = forms.IntegerField(min_value = 0, max_value = 100)
	x_2 = forms.IntegerField(min_value = 0, max_value = 100)
	y_1 = forms.IntegerField(min_value = 0, max_value = 100)
	y_2 = forms.IntegerField(min_value = 0, max_value = 100)


class sc_life_form(forms.Form):
	initial_altitdue = forms.FloatField(min_value = 200., max_value = 600.)
	mass = forms.FloatField(min_value = 0.0)
	area = forms.FloatField(min_value = 0.0)
	Cd = forms.FloatField(min_value = 0.0)
	total_impulse = forms.FloatField(min_value = 0.0)