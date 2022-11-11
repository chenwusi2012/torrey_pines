import webvtt
import pandas as pd
import metapy
import os
import shutil


SEGMENT_THRESHOLD = 30
LINK_PREFIX = "https://www.coursera.org/learn/cs-410/lecture/"


def convert_time(time_stamp):
    values = time_stamp.split(':')
    second = int(values[0]) * 3600 + int(values[1]) * 60 + int(values[2])
    return second


if __name__ == '__main__':
    print("Start parsing...")
    df = pd.DataFrame(columns=['lecture', 'lecture_id', 'start_time', 'end_time', 'text'])
    lecture_df = pd.read_csv('./dataset/link_info.csv')
    lecture_count = 0
    with open("./cs410/cs410.dat", "w") as file:
        for index, row in lecture_df.iterrows():
            segments_in_lecture = 0
            lecture = row['lecture']
            lecture_id = row['id']
            lecture_link = LINK_PREFIX + lecture_id
            print("Parsing ({}) {} ({})".format(lecture_count+1, lecture, lecture_link))
            update_start = True
            end = ''
            accu_text = ''
            filename = lecture + ".vtt"
            try:
                captions = webvtt.read('./subtitles/' + filename)
            except FileNotFoundError:
                print("Unable to find the file {}".format(filename))
            start = captions[0].start
            for idx, caption in enumerate(captions):
                start_time = caption.start[0:-4]
                end_time = caption.end[0:-4]
                text = caption.text
                text = text.replace('\n', ' ')
                # print(str(idx) + ": " + text)
                accu_text = accu_text + " " + text
                end = end_time
                if update_start:
                    start = start_time

                if idx == len(captions) - 1:
                    # print("***end of transcript, append***")
                    # print(start + " ----> " + end)
                    # print(accu_text)
                    df = df.append({'lecture': filename, 'lecture_id': lecture_id, 'start_time': start, 'end_time': end,
                                    'text': accu_text.strip()},
                                   ignore_index=True)
                    segments_in_lecture += 1
                    file.write(accu_text.strip() + "\n")
                elif text[-1] != '.':
                    # print("***not a dot, continue***")
                    update_start = False
                else:
                    if convert_time(end) - convert_time(start) >= SEGMENT_THRESHOLD:
                        # print("***find dot and long enough, append***")
                        # print(start + " ----> " + end)
                        # print(accu_text)
                        df = df.append(
                            {'lecture': filename, 'lecture_id': lecture_id, 'start_time': start, 'end_time': end,
                             'text': accu_text.strip()},
                            ignore_index=True)
                        segments_in_lecture += 1
                        file.write(accu_text.strip() + "\n")
                        accu_text = ''
                        update_start = True
                    else:
                        # print("***find dot but not long enough " + start + " ----> " + end + "***")
                        update_start = False
            lecture_count += 1
            print("Parsed {} segment(s) from this lecture".format(segments_in_lecture))
    df.to_csv('./dataset/data.csv')
    if os.path.exists('./idx/'):
        print("Old inverted index exist, remove old inverted index")
        shutil.rmtree('./idx/')
    print("Generating inverted index")
    idx = metapy.index.make_inverted_index('config.toml')
    print("==============================")
    print("Summary")
    print("==============================")
    print("Parsed {} lectures in total.".format(lecture_count))
    print("Parsed {} segments in total.".format(df.shape[0]))
    print("Total number of segments in inverted index: {}".format(idx.num_docs()))
