from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis, Range1d

from .forms import sc_life_form, delta_v_form


def sc_life(request):
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
			alt_final_range = np.arange(150., 510., 5)

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
			# # From Orbion atmospher tool for 0.4 solar cycle (range is for alts = np.arange(150, 510, 10))
			# rho = np.array([1.57503761e-09,   8.71650114e-10,   5.10685020e-10,
			#          3.11980283e-10,   1.96870776e-10,   1.27554367e-10,
			#          8.45030934e-11,   5.70666788e-11,   3.91884398e-11,
			#          2.73077516e-11,   1.92733000e-11,   1.37541417e-11,
			#          9.91009690e-12,   7.19947796e-12,   5.26742035e-12,
			#          3.87732881e-12,   2.86913243e-12,   2.13279450e-12,
			#          1.59179919e-12,   1.19229314e-12,   8.95975607e-13,
			#          6.75359621e-13,   5.10561785e-13,   3.87100189e-13,
			#          2.94364743e-13,   2.24542614e-13,   1.71855723e-13,
			#          1.32014841e-13,   1.01825680e-13,   7.89027203e-14,
			#          6.14600820e-14,   4.81574247e-14,   3.79887363e-14,
			#          3.01948922e-14,   2.42039447e-14,   1.95838940e-14])

			# From Orbion atmospher tool for 0.4 solar cycle (range is for alts = np.arange(150, 510, 5))
			rho = np.array([1.57503761e-09,   1.16186584e-09,   8.71650114e-10,
					         6.63182738e-10,   5.10685020e-10,   3.97346939e-10,
					         3.11980283e-10,   2.46935103e-10,   1.96870776e-10,
					         1.57990977e-10,   1.27554367e-10,   1.03554076e-10,
					         8.45030934e-11,   6.92878784e-11,   5.70666788e-11,
					         4.71978234e-11,   3.91884398e-11,   3.26573232e-11,
					         2.73077516e-11,   2.29073896e-11,   1.92733000e-11,
					         1.62604039e-11,   1.37541417e-11,   1.16620237e-11,
					         9.91009690e-12,   8.43869709e-12,   7.19947796e-12,
					         6.15309958e-12,   5.26742035e-12,   4.51607702e-12,
					         3.87732881e-12,   3.33331801e-12,   2.86913243e-12,
					         2.47239897e-12,   2.13279450e-12,   1.84167823e-12,
					         1.59179919e-12,   1.37705373e-12,   1.19229314e-12,
					         1.03316362e-12,   8.95975607e-13,   7.77596090e-13,
					         6.75359621e-13,   5.86994570e-13,   5.10561785e-13,
					         4.44403430e-13,   3.87100189e-13,   3.37435374e-13,
					         2.94364743e-13,   2.56991062e-13,   2.24542614e-13,
					         1.96355003e-13,   1.71855723e-13,   1.50551044e-13,
					         1.32014841e-13,   1.15879079e-13,   1.01825680e-13,
					         8.95795677e-14,   7.89027203e-14,   6.95890614e-14,
					         6.14600820e-14,   5.43604644e-14,   4.81574247e-14,
					         4.27338380e-14,   3.79887363e-14,   3.38344637e-14,
					         3.01948922e-14,   2.70038807e-14,   2.42039447e-14,
					         2.17451051e-14,   1.95838940e-14,   1.76824938e-14])

			# drag force
			F = 0.5 * rho * area * Cd * circular_velocity(alt_final_range) ** 2 # N

			# remaining velocity capability on-board divided by acceleration due to drag -> time
			life = remaining_DV / (F / m) * 3.17098e-8 # years

			# Create plot
			plot = figure(plot_width = 1000, plot_height = 800)

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

			return render(request, "sc_life_drag_plot.html", {"bokeh_plot_script": script, 'bokeh_plot_div': div})

	else:
		form = sc_life_form()

	return render(request, "sc_life_drag_plot.html", {'form': form})


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
			plot = figure(plot_width = 1000, plot_height = 800)

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

			return render(request, "delta_v_plot.html", {"bokeh_plot_script": script, 'bokeh_plot_div': div})

	else:
		form = delta_v_form()

	return render(request, "delta_v_plot.html", {'form': form})


def thruster_performance(request):
	return render(request, 'thruster_performance.html', {})