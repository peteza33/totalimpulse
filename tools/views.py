from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis, Range1d

from .forms import sc_drag_form, delta_v_form, thruster_performance_form, ep_prop_dutycycle_form


def sc_drag(request):
	if request.method == 'POST':
		form = sc_drag_form(request.POST)

		if form.is_valid():
			data = form.cleaned_data

			from tools import calcs
			import numpy as np
			import itertools

			"""
			User Inputs
			"""
			m = data['mass'] # kg
			area = data['area'] # m2
			Cd = data['Cd']
			life = data['Lifetime'] # years

			altitudes = np.arange(150, 505, 5)

			# impulse calc
			F_zero = 0.5 * calcs.rho_zero * area * Cd * calcs.circular_velocity_np_func(altitudes) ** 2
			F_five = 0.5 * calcs.rho_five * area * Cd * calcs.circular_velocity_np_func(altitudes) ** 2

			t = 3.154e7 * life

			impulse_drag_zero = F_zero * t
			impulse_drag_five = F_five * t 

			# drag plot
			drag = figure(
				plot_width = 1000, 
				plot_height = 800, 
				y_axis_label = 'Drag Force (N)',
				x_axis_label = 'Altitude (km)',
				title = 'Atmospheric Drag Force on a %.2f m2 and %.1f Cd Spacecraft' % (area, Cd),
				toolbar_location = "right",
				y_axis_type = 'log',
				)

			drag.line(altitudes, F_zero, legend = '0% Solar Cycle', color = 'blue')
			drag.line(altitudes, F_five, legend = '50% Solar Cycle', color = 'red')

			# formatting
			drag.title.align = "center"
			drag.toolbar.logo = None
			drag.legend.location = "top_right"
			drag.xaxis.axis_label_text_font_style = "normal"
			drag.yaxis.axis_label_text_font_style = "normal"
			drag.xaxis.axis_label_text_font_size = '12pt'
			drag.yaxis.axis_label_text_font_size = '12pt'
			drag.title.text_font_size = "12pt"
			
			# embed plot elements
			script_drag, div_drag = components(drag)


			# impulse plot
			impulse = figure(
				plot_width = 1000, 
				plot_height = 800, 
				y_axis_label = 'Total Impulse (kN-s)',
				x_axis_label = 'Altitude (km)',
				title = 'Total Impulse to Compensate for Drag Over %.1f Years' % life,
				toolbar_location = "right",
				y_axis_type = 'log',
			)

			impulse.line(altitudes, impulse_drag_zero / 1000, legend = '0% Solar Cycle', color = 'blue')
			impulse.line(altitudes, impulse_drag_five / 1000, legend = '50% Solar Cycle', color = 'red')

			# formatting
			impulse.title.align = "center"
			impulse.toolbar.logo = None
			impulse.legend.location = "top_right"
			impulse.xaxis.axis_label_text_font_style = "normal"
			impulse.yaxis.axis_label_text_font_style = "normal"
			impulse.xaxis.axis_label_text_font_size = '12pt'
			impulse.yaxis.axis_label_text_font_size = '12pt'
			impulse.title.text_font_size = "12pt"
			
			# embed plot elements
			script_impulse, div_impulse = components(impulse)


			# propellant
			propellant = figure(
				plot_width = 1000, 
				plot_height = 800, 
				y_axis_label = 'Prop Mass (kg)',
				x_axis_label = 'Altitude (km)',
				title = 'Propellant to Compensate for Drag Over %.1f Years at 0.5 Solar Cycle' % life,
				toolbar_location = "right",
				y_axis_type = 'log',
				)

			colors = itertools.cycle(('green', 'magenta', 'orange', 'blue', 'red', 'brown', 'darkorange'))

			for Isp in [250, 500, 1000, 1500]:
				propellant.line(altitudes, impulse_drag_five / (Isp * 9.806), legend = 'Isp = %s sec' % Isp, color = next(colors))

			# formatting
			propellant.title.align = "center"
			propellant.toolbar.logo = None
			propellant.legend.location = "top_right"
			propellant.xaxis.axis_label_text_font_style = "normal"
			propellant.yaxis.axis_label_text_font_style = "normal"
			propellant.xaxis.axis_label_text_font_size = '12pt'
			propellant.yaxis.axis_label_text_font_size = '12pt'
			propellant.title.text_font_size = "12pt"

			# embed plot elements
			script_propellant, div_propellant = components(propellant)

			return render(request, "sc_drag_plot.html", 
				{
				"script_drag": script_drag, "div_drag": div_drag,
				"script_impulse": script_impulse, 'div_impulse': div_impulse,
				"script_propellant": script_propellant, "div_propellant": div_propellant,
				})

	else:
		form = sc_drag_form()

	return render(request, "sc_drag_plot.html", {'form': form})


def delta_v(request):
	if request.method == 'POST':
		form = delta_v_form(request.POST)

		if form.is_valid():
			data = form.cleaned_data

			import numpy as np
			from tools import calcs
			
			# LV seperation altitude
			alt_initial = data['initial_altitude']

			# final mission operational altitude
			alt_final_range = np.arange(150., alt_initial, 10)
			
			# calc delta-V
			hohmann_transfer_DV = calcs.hohmann_transfer_np_func(alt_initial, alt_final_range)
			plane_change_to_maintain_SSO_DV = calcs.plane_change_to_maintain_SSO_np_func(alt_initial, alt_final_range)
			total_DV = hohmann_transfer_DV + plane_change_to_maintain_SSO_DV
			combined_alt_plane_change_SSO_DV = calcs.combined_alt_plane_change_SSO_np_func(alt_initial, alt_final_range)

			# Create plot
			plot = figure(
				plot_width = 1000, 
				plot_height = 800, 
				y_axis_label = 'Delta-V (m/s)',
				x_axis_label = 'Altitude (km)',
				title = 'Delta-V to Drop Altitude from %.0f km & Maintain SSO' % alt_initial,
				toolbar_location = "right",
			)

			# Add data
			plot.line(alt_final_range, hohmann_transfer_DV, legend = 'Hohmann Transfer', color = 'blue', line_dash = 'dashdot')
			plot.line(alt_final_range, plane_change_to_maintain_SSO_DV, legend = 'Plane Change to Maintain SSO', color = 'green', line_dash = 'dotdash')
			plot.line(alt_final_range, total_DV, color = 'red', legend = 'Hohmann + Plane Change (inefficient)', line_dash = 'dashed')
			plot.line(alt_final_range, combined_alt_plane_change_SSO_DV, color = 'orange', legend = 'Combining Altitude & Plane Change (most efficient)')

			# reverse the x-axis
			plot.x_range = Range1d(alt_initial, alt_final_range[0] - 10)

			# Formatting
			plot.title.align = "center"
			plot.toolbar.logo = None
			plot.legend.location = "top_left"
			plot.xaxis.axis_label_text_font_style = "normal"
			plot.yaxis.axis_label_text_font_style = "normal"
			plot.xaxis.axis_label_text_font_size = '12pt'
			plot.yaxis.axis_label_text_font_size = '12pt'
			plot.title.text_font_size = "12pt"
			
			# Embed plot elements
			script, div = components(plot)

			return render(request, "delta_v_plot.html", {"bokeh_plot_script": script, 'bokeh_plot_div': div})

	else:
		form = delta_v_form()

	return render(request, "delta_v_plot.html", {'form': form})


def thruster_performance(request):
	if request.method == 'POST':
		form = thruster_performance_form(request.POST)
		
		if form.is_valid():
			data = form.cleaned_data

			import numpy as np
			from scipy.integrate import ode
			from scipy.optimize import brentq
			import math

			# Inlet pressure range
			p_inlet = np.linspace(data['initial_inlet_pressure'], data['final_inlet_pressure'], 50)

			# Model mass flow rate
			k1 = data['k1'] 
			k2 = data['k2']
			def mdot_f(press):
				"""
				Output: kg/s
				"""
				return k1 * press ** k2

			"""
			IDEAL reults from RPA/CEA at 15 bar chamber pressure
			"""
			Ru = 8314 # J/kg-K
			Tci = data['Tci'] # K
			gamma = data['gamma']
			cstari = data['cstari'] # m/s
			cf = data['cf']
			Mw = data['MW'] # g/mol
			Cp = data['Cp'] # J/kg-K - at 1843 K

			# characteristic velocity (m/s)
			def cstar_f(Tc, gamma, Mw):
				return np.sqrt(Ru * Tc / (gamma * Mw * (2. / (gamma + 1.))**((gamma + 1.) / (gamma - 1.))))

			"""
			Model to estimate dynamic chamber energy balance. Makes estimates of the radiative area, emissivity and chamber thermal mass
			"""
			# Stefan-Boltzmann constant
			sigma = 5.67e-8 # W / m^2-K^4
			# gravity
			g0 = 9.806 # m / s^2
			# chamber diameter
			dc = data['dc'] # m (convert inches to m)
			# chamber length
			lc = data['lc'] # m (convert inches to m)
			# Wall area
			Ac = math.pi * dc * lc
			# heat transfer coefficient
			h = data['h'] # W/m^2-K
			# wall mass
			mw = data['wall_mass'] # kg
			# wall specific heat
			Cw = data['Cw'] # J/kg-K
			# space temp
			Tinf = 3. # K
			# ambient temp
			T0 = 273. # K

			# emissivity coefficient
			epsilon_f = lambda T: 0.9 - T / 3000.

			# combustion efficiency factor (used to make Isp = 231.5 at steady state with p_inlet = 22 (p_c = 15))
			# RPA/CEA results of overall estimated efficiency is 0.9417
			eta_c = data['eta_c']

			# Dynamic chamber energy balance
			def temp_dyn(mdot, Tw_i = 623., DC = 1., eta_c = 0.9, rate = 1., steps_per_period = 100):

				# enthalpy of reaction
				del_h_rxn = eta_c * Cp * (Tci - T0)

				# time
				tv = [0.0]

				# initial wall temp
				Tw = [Tw_i]

				# mass flow
				mdot_v = [mdot]

				# final time
				tf = rate * len(DC)

				def Tc_f(Tw, mdot_v):
					"""
					Combustion Temperature
					"""
					return (mdot_v*del_h_rxn + h*Ac*Tw + mdot_v*Cp*T0)/(mdot_v*Cp + h*Ac)

				def Tw_dot(t, Tw):
					'''
					Chamber Wall Temperature
					'''
					# Combustion temperature
					Tc = Tc_f(Tw, on*mdot)

					# Chamber wall temp with time
					dTw_dt = (h*Ac*(Tc-Tw) - sigma*epsilon_f(Tw)*Ac*(Tw**4 - Tinf**4)) / (mw*Cw)
					return dTw_dt

				# Pass chamber wall temperature function into ODE solver (runge-kutta)
				r = ode(Tw_dot).set_integrator('dopri5', atol=1e-3, rtol=1e-3, max_step=0.1, verbosity=1)

				# Set start temperature and start time
				r.set_initial_value(Tw_i, 0.0)

				# Count
				i = 0

				# Time step
				dt = 1. / rate / steps_per_period

				while r.successful() and r.t < tf and i < len(DC):
					# period's initial time
					tper_0 = r.t

					# Set thruster ON to include combustion heat flux
					on = 1.0
					for j in range(steps_per_period):

						# integrate over time step
						r.integrate(r.t + dt)

						# record time
						tv.append(r.t)

						# record wall temperature
						Tw.append(r.y)

						# record mass flow if engine is ON
						mdot_v.append(on * mdot)

						# check if thruster is ON for this time step
						if (r.t - tper_0) >= (DC[i] / rate):
						    on = 0.0
					i += 1
		    
				# combustion temperature
				Tc = Tc_f(np.array(Tw), np.array(mdot_v))

				# return time, wall temp, and mass flow
				return np.array(tv), np.array(Tw), Tc, np.array(mdot_v)

			"""
			Run the dynamic chamber temp energy balance 
			"""
			# Inlet pressure bar(a)
			Pf = data['maneuver_press'] # bar

			# Duration (sec)
			maneuver_time = data['maneuver_time'] # s

			# Duty Cycle (in percent)
			duty_cycle = data['duty_cycle']

			# Run combustion chamber energy balance
			tv, Tw, Tc, mdot_v = temp_dyn(mdot_f(Pf), eta_c = eta_c, DC = (np.ones([maneuver_time]) * duty_cycle))

			# characteristic velocity (m/s)
			cstar_t = cstar_f(Tc, gamma, Mw)

			# exhaust velocity (m/s)
			c_t = cstar_t * cf

			"""
			Plot
			"""
			plot = figure(
				plot_width = 1000, 
				plot_height = 800, 
				y_axis_label = 'Temperature (K)',
				x_axis_label = 'Time (sec)',
				title = 'Transient Model of Combustion Temperature and Performance',
				toolbar_location = "below",
				y_range = Range1d(600, 1600),
			)

			# primary axis
			plot.line(tv, Tc, legend = 'Gas Temp', color = 'red')
			plot.line(tv, Tw, legend = 'Wall Temp', color = 'blue', line_dash = 'dashdot')

			# secondary axis
			plot.extra_y_ranges = {"Isp": Range1d(start = 150, end = 250)}
			plot.add_layout(LinearAxis(y_range_name = "Isp", axis_label = "Specific Impulse (sec)"), 'right')

			plot.line(tv, c_t / g0, y_range_name = "Isp", legend = 'Isp', color = 'green', line_dash = 'dashed')

			# Formatting
			plot.title.align = "center"
			plot.toolbar.logo = None
			plot.legend.location = "bottom_right"
			plot.xaxis.axis_label_text_font_style = "normal"
			plot.yaxis.axis_label_text_font_style = "normal"
			plot.xaxis.axis_label_text_font_size = '12pt'
			plot.yaxis.axis_label_text_font_size = '12pt'
			plot.title.text_font_size = "12pt"
			
			# Embed plot elements
			script, div = components(plot)

			return render(request, "thruster_performance.html", {"bokeh_plot_script": script, 'bokeh_plot_div': div})
	
	else:
		form = thruster_performance_form()

	return render(request, "thruster_performance.html", {'form': form})


def ep_prop_dutycycle(request):
	if request.method == 'POST':
		form = ep_prop_dutycycle_form(request.POST)

		if form.is_valid():
			data = form.cleaned_data

			from tools import calcs
			import numpy as np
			import itertools

			# User inputs
			altitudes = np.arange(150, 505, 5)
			area = data['area']
			Cd = data['Cd']
			alt = data['altitude']
			eta_t = data['eta_t']

			Isps = np.arange(0, 5000, 25)

			density_dict = dict(zip(altitudes, calcs.rho_five))

			F = 0.5 * density_dict[alt] * area * Cd * calcs.circular_velocity_np_func(alt) ** 2

			powers = [50, 100, 150, 200, 300, 400, 500]

			colors = itertools.cycle(('green', 'magenta', 'orange', 'blue', 'red', 'brown', 'darkorange'))

			# Create plot2
			duty = figure(
				plot_width = 1000, 
				plot_height = 800, 
				y_axis_label = 'Duty Cycle',
				x_axis_label = 'Specific Impulse (sec)',
				title = 'Fraction of Mission Spent Thrusting to Compensate for Drag (%.0f km, 0.5 solar cycle) ' % alt,
				toolbar_location = "right",
				y_axis_type = 'log',
				y_range=(.01, 1)
			)

			# add data
			for i in powers:
				duty.line(Isps, (F * 9.806 * Isps) / (2 * eta_t * i), legend = '%.0f W' % i, color = next(colors))

			# formatting
			duty.title.align = "center"
			duty.toolbar.logo = None
			duty.legend.location = "bottom_right"
			duty.xaxis.axis_label_text_font_style = "normal"
			duty.yaxis.axis_label_text_font_style = "normal"
			duty.xaxis.axis_label_text_font_size = '12pt'
			duty.yaxis.axis_label_text_font_size = '12pt'
			duty.title.text_font_size = "12pt"

			# embed plot2 elements
			script, div = components(duty)

			return render(request, "ep_prop_dutycycle.html", {"bokeh_plot_script": script, 'bokeh_plot_div': div})

	else:
		form = ep_prop_dutycycle_form()

	return render(request, "ep_prop_dutycycle.html", {'form': form})