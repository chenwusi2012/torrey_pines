import metapy
import pandas as pd

LINK_PREFIX = "https://www.coursera.org/learn/cs-410/lecture/"
COUNT_THRESHOLD = 5


def convert_time(time_stamp):
    values = time_stamp.split(':')
    second = int(values[0]) * 3600 + int(values[1]) * 60 + int(values[2])
    return second


def search(keyword, top_count):
    idx = metapy.index.make_inverted_index('config.toml')
    #  print(idx.avg_doc_length())
    ranker = metapy.index.OkapiBM25(k1=1.2, b=0.75, k3=1.2)
    query = metapy.index.Document()
    query.content(keyword)
    top_docs = ranker.score(idx, query, num_results=top_count)
    #  print(top_docs)
    result = []
    for relevant_doc in top_docs:
        result.append(relevant_doc[0])
    return result


if __name__ == '__main__':
    indexes = search(keyword="bag of words", top_count=COUNT_THRESHOLD)
    df = pd.read_csv('./dataset/data.csv')
    rank = 1
    for index in indexes:
        sub_df = df.iloc[index]
        lecture = sub_df['lecture'][0:-4]
        start_time = sub_df['start_time']
        end_time = sub_df['end_time']
        text = sub_df['text']
        link = sub_df['lecture_id']
        link = LINK_PREFIX + link + "?t=" + str(convert_time(start_time))
        print(rank)
        print("INDEX: {}".format(index))
        print(lecture)
        print("{} ---> {}".format(start_time, end_time))
        print("{}...".format(text[0:-1]))
        print("LINK: {}".format(link))
        print("")
        rank += 1
