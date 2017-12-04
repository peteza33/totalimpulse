from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis, Range1d

from .forms import plot_line_form, sc_life_form, delta_v_form

def plots_home(request):
	return render(request, 'plot_home.html', {})


def plots_line(request):
	if request.method == 'POST':
		form = plot_line_form(request.POST)
		if form.is_valid():
			data = form.cleaned_data

			x_1 = data['x_1']
			x_2 = data['x_2']
			y_1 = data['y_1']
			y_2 = data['y_2']

			x = [x_1, x_2]
			y = [y_1, y_2]

			plot = figure(title = 'Line Plot', x_axis_label = 'X', y_axis_label = 'Y')

			plot.line(x, y)
			plot.circle(x, y)

			plot.toolbar.logo = None

			script, div = components(plot)

			return render(request, "plot_show.html", {"bokeh_plot_script": script, 'bokeh_plot_div': div})
	else:
		form = plot_line_form()
		plot_type = 'Line'

	return render(request, "plot_input_form.html", {'form': form, 'plot_type': plot_type})


def sc_life_plot(request):
	if request.method == 'POST':
		form = sc_life_form(request.POST)
		if form.is_valid():
			data = form.cleaned_data

			import numpy as np
			from math import pi, acos, sin, cos

			# acceleration due to gravity, m/s^2
			g0 = 9.806 

			# Earth radius, km
			radius_earth = 6371.135

			# mu = GM (standard gravitational parameter for Earth) km^3/s^2
			mu = 398600.4418

			# Standard maneuvers
			def circular_velocity(altitude):
			    """
			    Circular orbit, m/s
			    """
			    return np.sqrt(mu / (radius_earth + altitude)) * 1000

			def combined_alt_plane_change_SSO(initial_alt, final_alt):
			    """
			    efficient method (less total change in velocity) combine the plane change with the tangential burn at apogee of the transfer orbit, maintain SSO, m/s
			    """
			    desired_period = 365.2421896698 # tropical year (days)
			    
			    desired_nodal_regression_rate = -2 * pi / (desired_period * 86400) # rad/s
			    
			    J2 = 0.00108263
			    
			    initial_inclination = acos(desired_nodal_regression_rate * (radius_earth + initial_alt) ** 2 / \
			                               (1.5 * np.sqrt(mu/(radius_earth + initial_alt) ** 3) * radius_earth ** 2 * J2)) / pi * 180.
			    
			    final_inclination = acos(desired_nodal_regression_rate * (radius_earth + final_alt) ** 2 / \
			                               (1.5 * np.sqrt(mu/(radius_earth + final_alt) ** 3) * radius_earth ** 2 * J2)) / pi * 180.
			    
			    delta_inclination = initial_inclination - final_inclination
			    
			    return np.sqrt(circular_velocity(initial_alt) ** 2 + circular_velocity(final_alt) ** 2 - \
			    		2 * circular_velocity(initial_alt) * circular_velocity(final_alt) * cos(delta_inclination/180. * pi))

			# LV seperation altitude
			alt_initial = data['initial_altitdue']

			# final mission operational altitude
			alt_final_range = np.arange(150., 510., 10)

			# pass numpy arrays into python functions
			DV_function = np.vectorize(combined_alt_plane_change_SSO)

			# assume combined inclination & altitude change maneuvers (much more efficient)
			DV_alt_drop = DV_function(alt_initial, alt_final_range)

			"""
			Find life (time able to compensate for drag force) for each spacecraft design
			"""
			m = data['mass'] # kg
			area = data['area'] # m2
			Cd = data['Cd']
			total_impulse = data['total_impulse'] # N-s
			DV_capability = total_impulse / m # m/s
			    
			# DV for drag after dropping altitude to mission orbit
			remaining_DV = DV_capability - DV_alt_drop
			    
			"""
			Estimate drag force
			"""
			# Assumes atmosphere model from https://ccmc.gsfc.nasa.gov/modelweb/models/nrlmsise00.php
			# Total density taken for April 1, 2017 at 14:00 UTC
			# rho = np.array([2.322E-13, 1.657E-13, 1.204E-13, 8.892E-14, 6.659E-14, 5.047E-14, 3.867E-14, 2.991E-14, 2.333E-14,
			# 				1.834E-14, 1.452E-14, 1.156E-14, 9.256E-15, 7.448E-15, 6.021E-15, 4.886E-15, 3.980E-15, 3.252E-15,
			# 				2.665E-15, 2.190E-15, 1.805E-15, 1.490E-15, 1.233E-15, 1.022E-15, 8.492E-16, 7.066E-16, 5.890E-16,
			# 				4.918E-16, 4.113E-16, 3.445E-16, 2.890E-16]) * 1e2 **3 / 1e3

			# From Orbion atmospher tool for 0.4 solar cycle (range is for alts = np.arange(150, 510, 10))
			rho = np.array([1.57503761e-09,   8.71650114e-10,   5.10685020e-10,
			         3.11980283e-10,   1.96870776e-10,   1.27554367e-10,
			         8.45030934e-11,   5.70666788e-11,   3.91884398e-11,
			         2.73077516e-11,   1.92733000e-11,   1.37541417e-11,
			         9.91009690e-12,   7.19947796e-12,   5.26742035e-12,
			         3.87732881e-12,   2.86913243e-12,   2.13279450e-12,
			         1.59179919e-12,   1.19229314e-12,   8.95975607e-13,
			         6.75359621e-13,   5.10561785e-13,   3.87100189e-13,
			         2.94364743e-13,   2.24542614e-13,   1.71855723e-13,
			         1.32014841e-13,   1.01825680e-13,   7.89027203e-14,
			         6.14600820e-14,   4.81574247e-14,   3.79887363e-14,
			         3.01948922e-14,   2.42039447e-14,   1.95838940e-14])

			# drag force
			F = 0.5 * rho * area * Cd * circular_velocity(alt_final_range) ** 2 # N

			# remaining velocity capability on-board divided by acceleration due to drag -> time
			life = remaining_DV / (F / m) * 3.17098e-8 # years

			# Create plot
			plot = figure()

			# Add data
			plot.circle(alt_final_range, life, color = 'blue')
			plot.line(alt_final_range, life, legend = 'Lifetime', color = 'blue')

			plot.extra_y_ranges = {"drag": Range1d(start = 0, end = np.amax(F) * 1e3)}
			plot.add_layout(LinearAxis(y_range_name = "drag", axis_label = "Drag (mN)"), 'left')

			# secondary axis data
			plot.circle(alt_final_range, F * 1e3, y_range_name = "drag", color = 'red')
			plot.line(alt_final_range, F * 1e3, y_range_name = "drag", legend = 'Drag', color = 'red')

			# Formatting
			plot.title.text = 'SpaceCraft Life After Dropping Altitude from %.0f km' % alt_initial
			plot.title.align = "center"
			plot.xaxis.axis_label = "Altitude (km)"
			plot.yaxis.axis_label = "Time (years)"
			plot.toolbar.logo = None
			
			# Embed plot elements
			script, div = components(plot)

			return render(request, "plot_show.html", {"bokeh_plot_script": script, 'bokeh_plot_div': div})

	else:
		form = sc_life_form()
		plot_type = 'sc_drag_life'

	return render(request, "plot_input_form.html", {'form': form, 'plot_type': plot_type})


def delta_v(request):
	if request.method == 'POST':
		form = delta_v_form(request.POST)
		if form.is_valid():
			data = form.cleaned_data

			import numpy as np
			from math import pi, acos, sin, cos

			# acceleration due to gravity, m/s^2
			g0 = 9.806 

			# Earth radius, km
			radius_earth = 6371.135

			# mu = GM (standard gravitational parameter for Earth) km^3/s^2
			mu = 398600.4418

			# Standard maneuvers
			def circular_velocity(altitude):
				"""
				Circular orbit, m/s
				"""
				return np.sqrt(mu / (radius_earth + altitude)) * 1000

			def hohmann_transfer(initial_alt, final_alt):
				"""
				Hohmann transfer, most efficient circular & coplanar altitude change, m/s
				"""
				# semi-major axis of transfer ellipse
				initial_radius = radius_earth + initial_alt
				final_radius = radius_earth + final_alt
				a_transfer = (initial_radius + final_radius) / 2

				# velocity of transfer orbit at initial alt
				v_transfer_i = np.sqrt(mu * ((2 / initial_radius) - (1 / a_transfer)))

				# velocity of transfer orbit at final alt
				v_transfer_f = np.sqrt(mu * ((2 / final_radius) - (1 / a_transfer)))

				return (v_transfer_i - circular_velocity(initial_alt)) + (circular_velocity(final_alt) - v_transfer_f)

			def simple_plane_change(alt, inclination_change):
				"""
				inclination change (in degrees) with constant altitude, m/s
				"""
				return 2 * circular_velocity(alt) * sin((inclination_change / 180. * pi) / 2)

			def combined_alt_plane_change(initial_alt, final_alt, inclination_change):
				"""
				most efficient way of altitude + plane change (in degrees), m/s
				"""
				return np.sqrt(circular_velocity(initial_alt) ** 2 + circular_velocity(final_alt) ** 2 - \
				               2 * circular_velocity(initial_alt) * circular_velocity(final_alt) * cos(inclination_change / 180. * pi))

			# SSO specific manuevers
			def plane_change_to_maintain_SSO(initial_alt, final_alt):
				"""
				inclination adjustment to maintain SSO due to different altitude, m/s
				"""
				desired_period = 365.2421896698 # tropical year (days)

				desired_nodal_regression_rate = -2 * pi / (desired_period * 86400) # rad/s

				J2 = 0.00108263

				initial_inclination = acos(desired_nodal_regression_rate * (radius_earth + initial_alt) ** 2 / \
				                           (1.5 * np.sqrt(mu/(radius_earth + initial_alt) ** 3) * radius_earth ** 2 * J2)) / pi * 180
				final_inclination = acos(desired_nodal_regression_rate * (radius_earth + final_alt) ** 2 / \
				                           (1.5 * np.sqrt(mu/(radius_earth + final_alt) ** 3) * radius_earth ** 2 * J2)) / pi * 180
				delta_inclination = initial_inclination - final_inclination

				return 2 * circular_velocity(final_alt) * sin((delta_inclination / 180. * pi) / 2)

			def combined_alt_plane_change_SSO(initial_alt, final_alt):
				"""
				efficient method (less total change in velocity) combine the plane change with the tangential burn at apogee of the transfer orbit, maintain SSO, m/s
				"""
				desired_period = 365.2421896698 # tropical year (days)

				desired_nodal_regression_rate = -2 * pi / (desired_period * 86400) # rad/s

				J2 = 0.00108263

				initial_inclination = acos(desired_nodal_regression_rate * (radius_earth + initial_alt) ** 2 / \
				                           (1.5 * np.sqrt(mu/(radius_earth + initial_alt) ** 3) * radius_earth ** 2 * J2)) / pi * 180.

				final_inclination = acos(desired_nodal_regression_rate * (radius_earth + final_alt) ** 2 / \
				                           (1.5 * np.sqrt(mu/(radius_earth + final_alt) ** 3) * radius_earth ** 2 * J2)) / pi * 180.

				delta_inclination = initial_inclination - final_inclination

				return np.sqrt(circular_velocity(initial_alt) ** 2 + circular_velocity(final_alt) ** 2 - \
				               2 * circular_velocity(initial_alt) * circular_velocity(final_alt) * cos(delta_inclination/180. * pi))

			# LV seperation altitude
			alt_initial = data['initial_altitude']

			# final mission operational altitude
			alt_final_range = np.arange(150., alt_initial, 10)

			# vectorize python functionas
			hohmann_transfer_np_func = np.vectorize(hohmann_transfer)
			plane_change_to_maintain_SSO_np_func = np.vectorize(plane_change_to_maintain_SSO)
			combined_alt_plane_change_SSO_np_func = np.vectorize(combined_alt_plane_change_SSO)

			# calc delta-V
			hohmann_transfer_DV = hohmann_transfer_np_func(alt_initial, alt_final_range)
			plane_change_to_maintain_SSO_DV = plane_change_to_maintain_SSO_np_func(alt_initial, alt_final_range)
			total_DV = hohmann_transfer_DV + plane_change_to_maintain_SSO_DV
			combined_alt_plane_change_SSO_DV = combined_alt_plane_change_SSO_np_func(alt_initial, alt_final_range)

			# Create plot
			plot = figure()

			# Add data
			plot.line(alt_final_range, hohmann_transfer_DV, legend = 'Hohmann Transfer', color = 'blue')
			plot.line(alt_final_range, plane_change_to_maintain_SSO_DV, legend = 'Plane Change to Maintain SSO', color = 'green')
			plot.line(alt_final_range, total_DV, color = 'red', legend = 'Hohmann + Plane Change (inefficient)')
			plot.line(alt_final_range, combined_alt_plane_change_SSO_DV, color = 'orange', legend = 'Combining Altitude & Plane Change (most efficient)')

			# reverse the x-axis
			plot.x_range = Range1d(alt_initial, alt_final_range[0] - 10)

			# Formatting
			plot.title.text = 'Delta-V to Drop Altitude from %.0f km & Maintain SSO' % alt_initial
			plot.title.align = "center"
			plot.xaxis.axis_label = "Altitude (km)"
			plot.yaxis.axis_label = "Delta-V (m/s)"
			plot.toolbar.logo = None
			plot.legend.location = "top_left"
			
			# Embed plot elements
			script, div = components(plot)

			return render(request, "plot_show.html", {"bokeh_plot_script": script, 'bokeh_plot_div': div})

	else:
		form = delta_v_form()
		plot_type = 'delta_V'

	return render(request, "plot_input_form.html", {'form': form, 'plot_type': plot_type})
