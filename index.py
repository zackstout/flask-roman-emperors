
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

import re

df = pd.read_csv('emperors.csv', index_col=0, encoding='latin-1')

from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
app = Flask(__name__)

@app.route("/")
def hello():
    # return str(df.head(20)['name'])
    return render_template('index.html', taco = 'dog') # Note: must import this

# @app.route('/hi')
# def hi():
#     return "<h2>whatup</h2>"
#
# # This works correctly when we hit the route manually, but not when we ping it via AJAX...
# # We'll have to use hrefs with anchor tags to change the route URL.
# @app.route('/stuff')
# def yo():
#     val1 = request.args.get('val1')
#     val2 = request.args.get('val2')
#     return "<h2>%s, %s</h2>" % (val1, val2)



# NOTE: problem with "rise" because of ...multiple words? I'm pretty sure. Yeah, and multiple words break other queries as well. That's surely it.


# Populate the second selector:
@app.route('/getParticulars')
def here():
    choice = request.args.get('part')
    str_resp = str(set(df[choice]))
    result = str_resp.split(',')
    return str(result)

# Handle the full query, with type, particular and slice:
@app.route('/query')
def there(): # Interesting, names of these functions must be unique (across all routes??)
    type_x = request.args.get('type')
    choice_x = request.args.get('choice')
    slice_x = request.args.get('slice')

    type_space = re.sub('_', ' ', type_x)
    choice_space = re.sub('_', ' ', choice_x)
    slice_space = re.sub('_', ' ', slice_x)

    # Incredible: this is all we need to replicate the functionality that required sooooo much Node/PostgreSQL code...
    specific = df[df[type_space] == choice_space]
    result = specific.groupby(slice_space).count()['name']
    # I'm also surprised at how fast it is, given how long Python takes to spin up every time.
    return result.to_json(orient='split')


# Get average life/reign-span split by category (e.g. dynasty, cause of death...)
@app.route('/dataframe')
def df_stuff():
    # To return the entire dataframe as a json object (which I can't figure out how to parse...):
    # return df.to_json(orient='split')

    choice = request.args.get('choice')
    res = df.groupby(choice).mean()
    return str(res)

@app.route('/likelihood')
def like():
    type_x = request.args.get('type')
    choice = request.args.get('choice')
    choice_string = re.sub('_', ' ', choice)


    type_total = df.groupby(type_x).count()['name'].sum()
    choice_total = df[df[type_x] == choice_string].count()['name']

    # return str(choice_total) + type_x + choice + choice_string
    return str(choice_total)


# ADDING LIFESPANS AND REIGN-LENGTHS TO THE DATAFRAME -- should def be in own file/module:
spans = []

def getSpan(term):
    for row in df.iterrows():
        if term == 'life':
            start = row[1]['birth']
            end = row[1]['death']
        elif term == 'reign':
            start = row[1]['reign.start']
            end = row[1]['reign.end']

        if start == 'nan' or end == 'nan' or type(start).__name__ == 'float' or type(end).__name__ == 'float':
            global spans
            spans.append(0) # Changing this from 'nan' to 0 allows lifespans to be calculated numerically...will distort it somewhat, though.
            continue

        start = start.split('-')
        end = end.split('-')

        # This takes care of the BC problem, after also adding five "NEG"s to our csv:
        if 'NEG' in start[0]:
            start[0] = -(int(start[0][3:]))
        if 'NEG' in end[0]:
            end[0] = -(int(end[0][3:]))

        span = dict()
        span['years'] = int(end[0]) - int(start[0])
        span['months'] = int(end[1]) - int(start[1])
        span['days'] = int(end[2]) - int(start[2])

        if (span['months'] < 0):
            span['months'] = 12 + span['months']
            span['years'] -= 1

        if (span['days'] < 0):
            span['days'] = 30 + span['days']
            span['months'] -= 1

        days_in_term = span['years'] * 365 + span['months'] * 30 + span['days']

        spans.append(days_in_term)

def getReignLengths():
    getSpan('reign')

def getLifeSpans():
    getSpan('life')

def addToDF():
    global spans
    getLifeSpans()
    df['lifespan'] = pd.Series(spans, index=df.index)

    spans = []
    getReignLengths()
    df['reign'] = pd.Series(spans, index=df.index)
    # print(df.head())


# If we call this inside the route, it errors out the second time we try to ping it:
addToDF()








# # Then when the user clicks on a specific bar (e.g. Italia, 10), they can see the percentage of all those assassinated killed in Italia VS the overall percentage of Italians (Given that you're assassinated, what's the likelihood that you're from Italia? What's the overall likelihood of being from Italia?)
# # Could also show total assassinated percentage vs percentage of all those from Italia that were assassinated. (Given that you're from Italia, what's the likelihood you get assassinated? What's the overall likelihood of getting assassinated?)
#
# # Beautiful, this is how we get titles for the dropdown boxes:
# print(set(df['dynasty']))
#
# # Tells us how many 'cause' records we have:
# print(df.groupby('cause').count()['name'].sum())
# # Tells us how many assassinations we have:
# print(df[df['cause'] == 'Assassination'].count()['name'])

# Next steps:
# - Bring in (debugged) lifespan and reign-length to do correlation and averaging with those
# - use a display library like chart.js or d3 for visualization/interaction with the data







# Thanks SO:
# @app.route('/plot')
# def simple():
#     import datetime
#     from io import BytesIO # Had to use this instead of StringIO
#     import random
#     from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#     from matplotlib.figure import Figure
#     from matplotlib.dates import DateFormatter
#
#     fig = Figure()
#     ax = fig.add_subplot(111)
#     x = []
#     y = []
#     now=datetime.datetime.now()
#     delta=datetime.timedelta(days=1)
#     for i in range(10):
#         x.append(now)
#         now += delta
#         y.append(random.randint(0, 1000))
#     ax.plot_date(x, y, '-')
#     ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
#     fig.autofmt_xdate()
#     canvas=FigureCanvas(fig)
#     png_output = BytesIO() # Change to Bytes and delete method call
#     canvas.print_png(png_output)
#     response = make_response(png_output.getvalue()) # Note: must import this
#     response.headers['Content-Type'] = 'image/png'
#     return response


# This checks whether the script is being run directly or being called by another module:
if __name__ == "__main__":
    app.run()
