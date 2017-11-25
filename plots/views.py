from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.embed import components

import numpy as np

def simple_chart(request):
	x = np.linspace(0, 4*np.pi, 100)
	y = np.sin(x)

	plot = figure(title = "simple line example", x_axis_label = 'x', y_axis_label = 'y')

	plot.circle(x, y, legend = "sin(x)")
	plot.line(x, y, legend = "sin(x)")

	plot.line(x, 2*y, legend = "2*sin(x)", line_dash = [4, 4], line_color = "orange", line_width = 2)

	plot.square(x, 3*y, legend = "3*sin(x)", fill_color = None, line_color = "green")
	plot.line(x, 3*y, legend = "3*sin(x)", line_color = "green")

	plot.toolbar.logo = None

	script, div = components(plot)

	return render(request, "simple_chart.html", {"script": script, 'div': div})