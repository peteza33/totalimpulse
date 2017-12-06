from django import forms

class plot_line_form(forms.Form):
	x_1 = forms.IntegerField(min_value = 0, max_value = 100, initial = '5')
	x_2 = forms.IntegerField(min_value = 0, max_value = 100, initial = '10')
	y_1 = forms.IntegerField(min_value = 0, max_value = 100, initial = '15')
	y_2 = forms.IntegerField(min_value = 0, max_value = 100, initial = '20')


class sc_life_form(forms.Form):
	initial_altitdue = forms.FloatField(min_value = 150., max_value = 500., label = 'Initial Altitude (km)', initial = '500')
	mass = forms.FloatField(min_value = 0.0, label = 'Mass (kg)', initial = '110')
	area = forms.FloatField(min_value = 0.0, label = 'Wetted Area (m2)', initial = '0.57')
	Cd = forms.FloatField(min_value = 0.0, label = 'Coefficient of Drag (Cd)', initial = '2.2')
	total_impulse = forms.FloatField(min_value = 0.0, label = 'Total Impulse of System (N-s)', initial = '21000')

class delta_v_form(forms.Form):
	initial_altitude = forms.FloatField(min_value = 160., label = 'Initial Altitude (km)', initial = '500')