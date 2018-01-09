from django import forms

class sc_life_form(forms.Form):
	initial_altitdue = forms.FloatField(min_value = 150., max_value = 500., label = 'Initial Altitude (km)', initial = '500')
	mass = forms.FloatField(min_value = 0.0, label = 'Mass (kg)', initial = '110')
	area = forms.FloatField(min_value = 0.0, label = 'Wetted Area (m2)', initial = '0.57')
	Cd = forms.FloatField(min_value = 0.0, label = 'Coefficient of Drag (Cd)', initial = '2.2')
	total_impulse = forms.FloatField(min_value = 0.0, label = 'Total Impulse of System (N-s)', initial = '21000')

class delta_v_form(forms.Form):
	initial_altitude = forms.FloatField(min_value = 160., label = 'Initial Altitude (km)', initial = '500')

class thruster_performance_form(forms.Form):
	initial_inlet_pressure = forms.FloatField(min_value = 0, label = 'Beginning of Inlet Pressure Range (bar)', initial = '5.5')
	final_inlet_pressure = forms.FloatField(min_value = 0, label = 'Eng of Inlet Pressure Range (bar)', initial = '22')
	k1 = forms.FloatField(min_value = 0, label = 'Mass Flow Rate Coefficient K1 (kg/s)', initial = '3.78e-05')
	k2 = forms.FloatField(min_value = 0, label = 'Mass Flow Rate Coefficient K2 (kg/s)', initial = '0.82')
	Tci = forms.FloatField(min_value = 0, label = 'Ideal Combustion Temperature from CEA (K)', initial = '1843')
	gamma = forms.FloatField(min_value = 0, label = 'Ratio of Specific Heats from CEA (gamma)', initial = '1.228')
	cstari = forms.FloatField(min_value = 0, label = 'Ideal Characteristic Velocity from CEA (m/s)', initial = '1347.2')
	cf = forms.FloatField(min_value = 0, label = 'Coefficient of Thrust', initial = '1.8382')
	MW = forms.FloatField(min_value = 0, label = 'Molecular Weight (g/mol', initial = '19.718')
	Cp = forms.FloatField(min_value = 0, label = 'Specific Heat at Constant Pressure from CEA (J/kg-K)', initial = '2.2741e3')
	dc = forms.FloatField(min_value = 0, label = 'Chamber Diameter (m)', initial = '0.0127')
	lc = forms.FloatField(min_value = 0, label = 'Chamber Length (m)', initial = '0.0635')
	h = forms.FloatField(min_value = 0, label = 'Heat Transfer Coefficient (W/m^2-K)', initial = '500')
	wall_mass = forms.FloatField(min_value = 0, label = 'Chamber Wall Mass (kg)', initial = '0.01')
	Cw = forms.FloatField(min_value = 0, label = 'Chamber Wall Specific Heat (J/kg-K)', initial = '137')
	eta_c = forms.FloatField(min_value = 0, max_value = 1.0, label = 'Combustion Efficieny (Eta)', initial = '0.94')
	maneuver_press = forms.FloatField(min_value = 0, label = 'Maneuver Pressure to Simulate (bar)', initial = '18.5')
	maneuver_time = forms.IntegerField(min_value = 0, label = 'Maneuver Time to Simulate (sec)', initial = '10')
	duty_cycle = forms.FloatField(min_value = 0, label = 'Maneuver Duty Cycle to Simulate (0.0 to 1.0)', initial = '1.0')

class ep_prop_dutycycle_form(forms.Form):
	isp = forms.FloatField(min_value = 0, max_value = 10000, label = 'Specific Impulse (sec)', initial = '1000')
	area = forms.FloatField(min_value = 0.0, label = 'Wetted Area (m2)', initial = '0.57')
	Cd = forms.FloatField(min_value = 0.0, label = 'Coefficient of Drag (Cd)', initial = '2.2')
	time = forms.FloatField(min_value = 0.0, label = 'Duration (days)', initial = '365')
	eta_t = forms.FloatField(min_value = 0.0, max_value = 1.0, label = 'Total Efficiency (for Duty Cycle)', initial = '0.3')
	altitude = forms.FloatField(min_value = 150, max_value = 500, label = 'Altitude (for Duty Cycle) (km)', initial = '250')