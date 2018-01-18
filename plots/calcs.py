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


# Vectorized maneuvers
circular_velocity_np_func = np.vectorize(circular_velocity)
hohmann_transfer_np_func = np.vectorize(hohmann_transfer)
plane_change_to_maintain_SSO_np_func = np.vectorize(plane_change_to_maintain_SSO)
combined_alt_plane_change_SSO_np_func = np.vectorize(combined_alt_plane_change_SSO)

# 0.0 solar cycle (range is for alts = np.arange(150, 505, 5))
rho_zero = np.array([1.44347741e-09,   1.04764962e-09,   7.71345025e-10,
			         5.74650093e-10,   4.32449162e-10,   3.28289494e-10,
			         2.51164218e-10,   1.93523802e-10,   1.50092876e-10,
			         1.17127958e-10,   9.19382945e-11,   7.25688416e-11,
			         5.75859763e-11,   4.59300563e-11,   3.68123490e-11,
			         2.96420485e-11,   2.39740231e-11,   1.94710536e-11,
			         1.58763274e-11,   1.29931031e-11,   1.06705357e-11,
			         8.79145466e-12,   7.26503829e-12,   6.02035595e-12,
			         5.00176412e-12,   4.16539519e-12,   3.47650131e-12,
			         2.90743047e-12,   2.43607781e-12,   2.04469525e-12,
			         1.71895592e-12,   1.44731175e-12,   1.22032817e-12,
			         1.03032551e-12,   8.71019606e-13,   7.37250307e-13,
			         6.24770025e-13,   5.30069397e-13,   4.50243625e-13,
			         3.82882121e-13,   3.25980058e-13,   2.77866730e-13,
			         2.37147305e-13,   2.02655304e-13,   1.73413717e-13,
			         1.48603060e-13,   1.27535092e-13,   1.09631104e-13,
			         9.44039541e-14,   8.14431679e-14,   7.04025501e-14,
			         6.09898680e-14,   5.29582431e-14,   4.60989579e-14,
			         4.02354349e-14,   3.52181902e-14,   3.09205991e-14,
			         2.72353388e-14,   2.40713955e-14,   2.13515458e-14,
			         1.90102344e-14,   1.69916203e-14,   1.52487562e-14,
			         1.37412140e-14,   1.24347883e-14,   1.13003741e-14,
			         1.03131948e-14,   9.45214898e-15,   8.69925705e-15,
			         8.03919219e-15,   7.45888270e-15])

# 0.5 solar cycle (range is for alts = np.arange(150, 505, 5))
rho_five = np.array([1.58264665e-09,   1.16881797e-09,   8.78106152e-10,
			         6.69203234e-10,   5.16288417e-10,   4.02536185e-10,
			         3.16757074e-10,   2.51305457e-10,   2.00846547e-10,
			         1.61589433e-10,   1.30796989e-10,   1.06465150e-10,
			         8.71084107e-11,   7.16136459e-11,   5.91386812e-11,
			         4.90408193e-11,   4.08257602e-11,   3.41106326e-11,
			         2.85969353e-11,   2.40505319e-11,   2.02867271e-11,
			         1.71590341e-11,   1.45505131e-11,   1.23680947e-11,
			         1.05362177e-11,   8.99404093e-12,   7.69216339e-12,
			         6.59030507e-12,   5.65548970e-12,   4.86061497e-12,
			         4.18328493e-12,   3.60507073e-12,   3.11054994e-12,
			         2.68690192e-12,   2.32340944e-12,   2.01108441e-12,
			         1.74236975e-12,   1.51089178e-12,   1.31126346e-12,
			         1.13892052e-12,   9.89987339e-13,   8.61166306e-13,
			         7.49646281e-13,   6.53026561e-13,   5.69253570e-13,
			         4.96567972e-13,   4.33460363e-13,   3.78634053e-13,
			         3.30973726e-13,   2.89518978e-13,   2.53441927e-13,
			         2.22028231e-13,   1.94660953e-13,   1.70806832e-13,
			         1.50004568e-13,   1.31854822e-13,   1.16011657e-13,
			         1.02175202e-13,   9.00853668e-14,   7.95164337e-14,
			         7.02724143e-14,   6.21823489e-14,   5.50998020e-14,
			         4.88952255e-14,   4.34566941e-14,   3.86868047e-14,
			         3.45007588e-14,   3.08247041e-14,   2.75942982e-14,
			         2.47534645e-14,   2.22533138e-14])
