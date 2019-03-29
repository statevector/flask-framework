from flask import Flask, render_template, request, redirect

import random

from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid, Range1d)
#from bokeh.models.glyphs import VBar
from bokeh.plotting import figure, output_file, show
#from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool

#from bokeh.io import output_notebook
#output_notebook()

# connect the app
app = Flask(__name__)

# the plotting function
def MakePlot(data):

    source = ColumnDataSource(data)
    print(source.column_names)

    #source = ColumnDataSource(dict(
    #    x = data.weight_kgs, 
    #    y = data.height_m,
    #)

    #PLOT_OPTS = dict(
    #    height=400, 
    #    x_axis_type='log', 
    #    y_axis_type='log', 
    #    y_range=(0.08,20), 
    #    x_range=(0.08,2000)
    #)

    hover = HoverTool(tooltips = [
        ('days','@days'),
        ('bugs','@bugs'),
        ('costs','@costs')], 
        show_arrow=False)

    #p = figure(title='Pokémon',
    #    x_axis_label='Weight [kg]',
    #    y_axis_label='Height [m]',
    #    title_location='above',
    #    toolbar_location='right',
    #    tools=[hover], **PLOT_OPTS)

    # create a new plot with a title and axis labels
    p = figure(plot_height=250, title="Bug Counts",
           toolbar_location=None, tools=[hover])
    #p = figure(tools=[hover], **PLOT_OPTS)

    p.vbar(x='days', top='bugs', width=0.9, source=source)
    #p.circle(x='x', y='y', source=source, size=10, alpha=0.8, line_color='black', fill_color='pink')

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    #hover = create_hover_tool()
    #plot = create_bar_chart(data, "Bugs per day", "days", "bugs", hover)

    # return the finalized plot
    return p


# the homepage
@app.route('/')
def homepage():

	# get the data, from somewhere...
    # (here, dictionary mapping string to list)
    bars_count = 11
    data = {'days': [], 'bugs': [], 'costs': []}
    for i in range(1, bars_count + 1):
        data['days'].append(i)
        data['bugs'].append(random.randint(1,100))
        data['costs'].append(random.uniform(1.00, 1000.00))

    # setup the plot
    p = MakePlot(data)
    script, div = components(p)

    print(script)
    print(div)

    # render the html page
    return render_template("chart.html", the_div=div, the_script=script)











#@app.route('/')
#def index():
#    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath



#if __name__ == "__main__":
#    app.run(debug=True)

if __name__ == '__main__':
 	app.run(port=33507)






