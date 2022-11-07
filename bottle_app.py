from bottle import route, run, template, request
import pandas as pd
import metapy
import datetime

df = pd.read_csv('./dataset/data.csv')
print("Dataframe loaded")

LINK_PREFIX = "https://www.coursera.org/learn/cs-410/lecture/"
COUNT_THRESHOLD = 10


def convert_time(time_stamp):
    values = time_stamp.split(':')
    second = int(values[0]) * 3600 + int(values[1]) * 60 + int(values[2])
    return second


def rank(query_terms, top_count):
    idx = metapy.index.make_inverted_index('config.toml')
    ranker = metapy.index.OkapiBM25(k1=1.2, b=0.75, k3=1.2)
    query = metapy.index.Document()
    query.content(query_terms)
    top_docs = ranker.score(idx, query, num_results=top_count)
    result = []
    for relevant_doc in top_docs:
        result.append(relevant_doc[0])
    return result


@route('/')
def root():
    print("Home page")
    return template('home')


@route('/search', method='POST')
def search():
    a = datetime.datetime.now()
    print("Result page")
    query = request.forms.get('query')
    print("QUERY: '{}'".format(query))
    indexes = rank(query, COUNT_THRESHOLD)
    result = []
    print("INDEX: {}".format(indexes))
    for index in indexes:
        segment = {}
        sub_df = df.iloc[index]
        segment['lecture'] = sub_df['lecture'][0:-4]
        segment['start_time'] = sub_df['start_time']
        segment['end_time'] = sub_df['end_time']
        segment['text'] = sub_df['text']
        link = sub_df['lecture_id']
        segment['link'] = LINK_PREFIX + link + "?t=" + str(convert_time(segment['start_time']))
        segment['index'] = index
        result.append(segment)
    print("Result collected, display on webpage...")
    b = datetime.datetime.now()
    c = b - a
    time_delta = c.seconds + c.microseconds / 1000000
    print("SEARCH TIME: {}".format(time_delta))
    return template('result', query=query, result=result, time_delta=time_delta)


run(host='localhost', port=8080, debug=True)
