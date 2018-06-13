
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

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

@app.route('/hi')
def hi():
    return "<h2>whatup</h2>"

# This works correctly when we hit the route manually, but not when we ping it via AJAX...
# We'll have to use hrefs with anchor tags to change the route URL.
@app.route('/stuff')
def yo():
    val1 = request.args.get('val1')
    val2 = request.args.get('val2')
    return "<h2>%s, %s</h2>" % (val1, val2)



# # This is the meat of our query:
# specific2 = df[df['rise'] == 'Appointment by Army']
# specific3 = df[df['cause'] == 'Assassination']
# specific4 = df[df['birth.prv'] == 'Italia']
# specific5 = df[df['cause'] == 'Assassination']
#
# print(specific4.groupby('cause').count()['name'])
#
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






# Thanks SO:
@app.route('/plot')
def simple():
    import datetime
    from io import BytesIO # Had to use this instead of StringIO
    import random
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig = Figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now += delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = BytesIO() # Change to Bytes and delete method call
    canvas.print_png(png_output)
    response = make_response(png_output.getvalue()) # Note: must import this
    response.headers['Content-Type'] = 'image/png'
    return response



if __name__ == "__main__":
    app.run()
