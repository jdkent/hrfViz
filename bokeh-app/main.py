''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``hrf`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from nistats import hemodynamic_models

# Set up data
model = hemodynamic_models._gamma_difference_hrf(tr=2)
x = np.arange(0, len(model))
source = ColumnDataSource(data=dict(x=x, y=model))


# Set up plot
thr = 0.01
plot = figure(plot_height=400, plot_width=400, title="my hrf wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, np.max(x)], y_range=[np.min(model)-thr, np.max(model)+thr])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="title", value='my hrf')
delay = Slider(title="delay", value=6.0, start=0, end=10, step=0.1)
time_length = Slider(title="time_length", value=32.0, start=16, end=48, step=0.1)
onset = Slider(title="onset", value=0.0, start=0.0, end=10, step=0.1)
undershoot = Slider(title="undershoot", value=16.0, start=4, end=32, step=0.1)
dispersion = Slider(title="dispersion", value=1.0, start=0.1, end=5.0, step=0.1)
u_dispersion = Slider(title="u_dispersion", value=1.0, start=0.1, end=5.0, step=0.1)
ratio = Slider(title="ratio", value=0.167, start=0.01, end=2.0, step=0.1)
scale = Slider(title="amplitude", value=1, start=0, end=5, step=0.1)

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value


text.on_change('value', update_title)


def update_data(attrname, old, new):

    # Get the current slider values
    dy = delay.value
    tl = time_length.value
    on = onset.value
    un = undershoot.value
    di = dispersion.value
    ud = u_dispersion.value
    ra = ratio.value

    # Generate the new curve
    model = hemodynamic_models._gamma_difference_hrf(
        tr=2, time_length=tl, onset=on, delay=dy, undershoot=un,
        dispersion=di, u_dispersion=ud, ratio=ra
        )
    x = np.arange(0, len(model)) * scale.value
    source.data = dict(x=x, y=model)


for w in [delay, time_length, onset, delay, undershoot, dispersion, u_dispersion, ratio, scale]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = column(text, delay, time_length, onset,
                delay, undershoot, dispersion, u_dispersion, ratio,
                scale)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "My HRF"
