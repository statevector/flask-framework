from flask import Flask, render_template, request, redirect, url_for

import random
import pandas as pd
import requests
import quandl

from bokeh.models import FactorRange, Plot, LinearAxis, Grid
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool

# connect the app
app = Flask(__name__)

# the dataframe function
def get_data(ticker_symbol, columns):

    # your API key goes here
    quandl.ApiConfig.api_key = 'Y-vgM5syW3N9KmRk7nZY'

    data = quandl.get_table('WIKI/PRICES', 
        qopts = { 'columns': columns},
        ticker = [ticker_symbol], 
        date = { 'gte': '2017-01-01', 'lte': '2017-12-31' }, paginate=True)

    return data


# the plotting function
def make_plot(data):

    # set the Bokeh column data source
    source = ColumnDataSource(data)
    print(source.column_names)

    # set the tools
    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"

    # initialize the canvas for plotting
    p1 = figure(x_axis_type="datetime", title="Quandl WIKI EOD Stock Prices - 2017", tools=[TOOLS])
    p1.grid.grid_line_alpha = 0.6
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    ticker = str(data.iloc[0]['ticker'])
    #print(ticker)

    # plot only what the user has selected
    if 'open' in data.columns: 
    	p1.line(data['date'], data['open'], color='orange', legend=ticker+': open')
    if 'close' in data.columns: 
    	p1.line(data['date'], data['close'], color='blue', legend=ticker+': close')
    if 'adj_open' in data.columns: 
    	p1.line(data['date'], data['adj_open'], color='red', legend=ticker+': adj_open')
    if 'adj_close' in data.columns: 
    	p1.line(data['date'], data['adj_close'], color='green', legend=ticker+': adj_close')
    
    p1.legend.location = 'top_left'

    # return the finalized plot
    return p1

# the homepage
@app.route('/')
def homepage():
    return render_template('login.html')

# the homepage after POST request
@app.route('/', methods=['POST'])
def plotpage():

    # get the submitted form values...
    ticker_symbol = request.form.get('ticker')
    close_price = request.form.get('close')
    open_price = request.form.get('open')
    adj_close_price = request.form.get('adj_close')
    adj_open_price = request.form.get('adj_open')

    # .. and put them a list, removing any 'None' entries
    columns = ['ticker', 'date', open_price, close_price, adj_close_price, adj_open_price]
    columns = [col for col in columns if col is not None]

    # build the dataframe using the submitted values
    data = get_data(ticker_symbol, columns)
    print(data)

    # make the plot and extract its components for HTML rendering
    p = make_plot(data)
    script, div = components(p)
    #print(script)
    #print(div)

    # render the HTML page with the plot embedded
    return render_template("chart.html", the_div=div, the_script=script)


#if __name__ == "__main__":
#    app.run(debug=True)

if __name__ == '__main__':
 	app.run(port=33507)
