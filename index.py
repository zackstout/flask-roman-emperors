
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
@app.route('/stuff')
def yo():
    val1 = request.args.get('val1')
    val2 = request.args.get('val2')
    return "<h2>%s, %s</h2>" % (val1, val2)











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
