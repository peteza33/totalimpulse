from django.shortcuts import render

from bokeh.plotting import figure
from bokeh.embed import components

def simple_chart(request):
	x = [1, 2, 3, 4, 5]
	y = [6, 7, 2, 4, 5]

	# create a new plot with a title and axis labels
	p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

	# add a line renderer with legend and line thickness
	p.line(x, y, legend="Temp.", line_width=2)

	script, div = components(p)

	return render(request, "simple_chart.html", {"the_script": script, "the_div": div})