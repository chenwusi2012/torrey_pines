from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

LINK_PREFIX = "https://www.coursera.org/learn/cs-410/lecture/"
COUNT_THRESHOLD = 5

app = Flask(__name__)


def convert_time(time_stamp):
    values = time_stamp.split(':')
    second = int(values[0]) * 3600 + int(values[1]) * 60 + int(values[2])
    return second


def rank(query_terms, top_count):
    import metapy
    idx = metapy.index.make_inverted_index('config.toml')
    print("1")
    ranker = metapy.index.OkapiBM25(k1=1.2, b=0.75, k3=1.2)
    print("2")
    query = metapy.index.Document()
    query.content(query_terms)
    print("3")
    top_docs = ranker.score(idx, query, num_results=top_count)
    print("4")
    result = []
    for relevant_doc in top_docs:
        result.append(relevant_doc[0])
    return result


@app.route('/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        query = request.form.get("query")
        query = query.replace(" ", "+")
        return redirect(url_for('search', query=query))
    return render_template("home.html")


@app.route('/search/<query>')
def search(query):
    query = query.replace("+", " ")
    query = query.strip()
    print("QUERY: {}".format(query))
    # indexes = [28, 32]
    indexes = rank(query, COUNT_THRESHOLD)
    print("INDEX: {}".format(indexes))
    df = pd.read_csv('./dataset/data.csv')
    result = []
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
    return render_template('result.html', query=query, result=result)


if __name__ == '__main__':
    app.run(debug=False)
