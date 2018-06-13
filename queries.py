
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

filename = 'emperors.csv'
# strfile = unicode(str(filename), errors='replace')
df = pd.read_csv('../emperors.csv', index_col=0, encoding='latin-1')


# ***** I'm thinking we need Python running the server itself to be able to respond to AJAX requests from the client... *****

def main():
    # print(df['name'])
    # print(df.axes)

    for row in df.iterrows():
        print(row[1]['reign.start'], '\n')

    # print(df.describe())

# if __name__ == "__main__":
#     x=main()
#     return x;

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
            spans.append('nan')
            # return
            continue # not sure why this is stopping at the first nan....Ah, need continue instead of break.

        start = start.split('-')
        end = end.split('-')

        # print(row[1]['name'])

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

        # print(span)

        days_in_term = span['years'] * 365 + span['months'] * 30 + span['days']
        # print(days_in_term)

        # Not sure why this isn't working....
        # if term == 'life':
        #     row[1]['lifespan'] = days_in_term
        # elif term == 'reign':
        #     row[1]['reign.term'] = days_in_term
        spans.append(days_in_term)
    # print("spansssssss: ", spans) # Why won't this print out right here????
    # print('hi h i hi hi')


# I believe this is working correctly:
def getReignLengths():
    getSpan('reign')


# getReignLengths()

def getLifeSpans():
    getSpan('life')

# getLifeSpans()



def groupByEra():
    for row in df.iterrows():
        print(row[1]['dynasty'])

# groupByEra()

def getGroups(term):
    for thing in df.groupby([term]):
        print(thing[0])
    # print(df.groupby(["dynasty"]))

    # print(df.count())

# getGroups('killer')


# Good: This grabs only a specific group (those assassinated) grouped by dynasty:
def sumRows(term):
    specific = df[df['cause'] == 'Assassination']

    specific2 = df[df['rise'] == 'Seized Power']
    # print(summed)
    print(specific2.groupby(term).count()['name'])
    # print(df.groupby(term).count()['name'])


# sumRows('cause') # This is asking, of those who seized power, how did they die?


# When is reign end not equal to death?

def deathIsEnd():
    for row in df.iterrows():
        death = row[1]['death']
        end = row[1]['reign.end']
        print(row[1]['name'], death == end)

# deathIsEnd()


# Note: will need to run this before any other functions that try to access lifespan/reign length columns:
def addToDF():
    global spans

    getLifeSpans()
    # print(df.head())
    # print(spans)
    df['lifespan'] = pd.Series(spans, index=df.index)
    # print(df.head())

    spans = []

    getReignLengths()
    df['reign'] = pd.Series(spans, index=df.index)
    print(df.head())

    avg_reign_length = df['reign'].sum() / len(df['reign'])
    # avg_life_span = df[df['lifespan'] != 'nan'].sum() / len(df['lifespan']) # won't work because of strings??
    print(avg_reign_length)


addToDF()

def reignByDyn():
    # print(df.head())
    dyns = df.groupby('dynasty')
    print(dyns)
    for d in dyns:
        print(d[1])

reignByDyn()


def playWithGB():
    dyns = df.groupby('dynasty').mean()
    print(dyns)

    # Same result as above:
    dyns2 = df.groupby('dynasty').agg(np.mean)
    print(dyns2)

    # Hmm only getting one column....
    # print(df.corr())



# Thank you https://www.dataquest.io/blog/pandas-python-tutorial/:
# - df.iloc
# -reviews.loc[:5,["score", "release_year"]]
# -reviews[["score", "release_year"]]
# -Create a df by passing multiple series to the DF constructor
# -reviews["score"].mean()
# -reviews.mean()
# -pandas.DataFrame.corr — finds the correlation between columns in a DataFrame.
# -pandas.DataFrame.count — counts the number of non-null values in each DataFrame column.
# -pandas.DataFrame.max — finds the highest value in each column.
# -pandas.DataFrame.min — finds the lowest value in each column.
# -pandas.DataFrame.median — finds the median of each column.
# -pandas.DataFrame.std — finds the standard deviation of each column.
# -score_filter = reviews["score"] > 7
# -filtered_reviews = reviews[score_filter]
# -xbox_one_filter = (reviews["score"] > 7) & (reviews["platform"] == "Xbox One")
# reviews[reviews["platform"] == "Xbox One"]["score"].plot(kind="hist")
# filtered_reviews["score"].hist()




# Dictionaries can be converted easily into Series.
# Boolean indexing: cities[cities > 1000]
# Pass a dictionary of lists to the Dataframes constructor












# box/whisker -- Wow this is amazing:
# df.plot(kind='box', subplots=True, layout=(3, 3), sharex=False, sharey=False)
# plt.show()

# histograms -- Wow this is also nuts:
# df.hist()
# plt.show()

# scatter plot matrix -- WOW --:
# scatter_matrix(df)
# plt.show()



# would be good to write a function that checks how many of those (e.g.) from Italia assassinated, VS how often *everyone* was assassinated.
