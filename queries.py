
def getSpan(term):
    for row in df.iterrows():
        if term == 'life':
            start = row[1]['birth']
            end = row[1]['death']
        elif term == 'reign':
            start = row[1]['reign.start']
            end = row[1]['reign.end']

        if start == 'nan' or end == 'nan' or type(start).__name__ == 'float' or type(end).__name__ == 'float':
            return

        start = start.split('-')
        end = end.split('-')

        print(row[1]['name'])

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
        print(days_in_term)

        # Not sure why this isn't working....
        if term == 'life':
            row[1]['lifespan'] = days_in_term
        elif term == 'reign':
            row[1]['reign.term'] = days_in_term


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


sumRows('cause') # This is asking, of those who seized power, how did they die?


# When is reign end not equal to death?

def deathIsEnd():
    for row in df.iterrows():
        death = row[1]['death']
        end = row[1]['reign.end']
        print(row[1]['name'], death == end)

# deathIsEnd()


def getAvgLifeSpan():
    getLifeSpans()
    print(df.head())

# getAvgLifeSpan()
