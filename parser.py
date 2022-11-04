import webvtt
import pandas as pd

SEGMENT_THRESHOLD = 30


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
            lecture = row['lecture']
            lecture_id = row['id']
            print("Parsing {} ({})".format(lecture, lecture_id))
            update_start = True
            end = ''
            accu_text = ''
            filename = lecture + ".vtt"
            captions = webvtt.read('./subtitles/' + filename)
            start = captions[0].start
            # print(len(captions))
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
                        file.write(accu_text.strip() + "\n")
                        accu_text = ''
                        update_start = True
                    else:
                        # print("***find dot but not long enough " + start + " ----> " + end + "***")
                        update_start = False
            lecture_count += 1
    df.to_csv('./dataset/data.csv')
    print("Parsed {} lectures in total.".format(lecture_count))
    print("Parsed {} segments in total.".format(df.shape[0]))
