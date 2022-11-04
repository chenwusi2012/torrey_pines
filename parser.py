import webvtt
import pandas as pd


def convert_time(time_stamp):
    values = time_stamp.split(':')
    second = int(values[0]) * 3600 + int(values[1]) * 60 + int(values[2])
    return second


if __name__ == '__main__':
    df = pd.DataFrame(columns=['lecture', 'start_time', 'end_time', 'text'])
    update_start = True
    end = ''
    accu_text = ''
    filename = 'Lesson 1.2 Text Access.vtt'
    captions = webvtt.read('./subtitles/' + filename)
    start = captions[0].start
    print(len(captions))
    for idx, caption in enumerate(captions):
        start_time = caption.start[0:-4]
        end_time = caption.end[0:-4]
        text = caption.text
        text = text.replace('\n', ' ')
        print(str(idx) + ": " + text)
        if text != '[SOUND]' and text != '[MUSIC]':
            accu_text = accu_text + " " + text
            end = end_time
            if update_start:
                start = start_time
            if text[-1] != '.':
                print("***not a dot, continue***")
                update_start = False
            else:
                if convert_time(end) - convert_time(start) >= 30 or idx == len(captions)-2:
                    print("***find dot and long enough, append***")
                    df = df.append(
                        {'lecture': filename, 'start_time': start, 'end_time': end, 'text': accu_text.strip()},
                        ignore_index=True)
                    print(start + " ----> " + end)
                    print(accu_text)
                    accu_text = ''
                    update_start = True
                else:
                    print("***find dot but not long enough " + start + " ----> " + end + "***")
                    update_start = False
        else:
            update_start = True
    df.to_csv('./dataset/data.csv')
