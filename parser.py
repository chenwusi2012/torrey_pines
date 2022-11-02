import webvtt
import pandas as pd

if __name__ == '__main__':
    update_start = True
    start = ''
    end = ''
    accu_text = ''
    df = pd.DataFrame(columns=['lecture', 'start_time', 'end_time', 'text'])
    filename = 'Lesson 1.2 Text Access.vtt'
    captions = webvtt.read('./subtitles/' + filename)
    start = captions[0].start
    for idx, caption in enumerate(captions):
        start_time = caption.start[0:-4]
        end_time = caption.end[0:-4]
        text = caption.text
        text = text.replace('\n', ' ')
        print("start time: " + start_time)
        print("end time: " + end_time)
        print("text: " + text)
        if text != '[SOUND]' and text != '[MUSIC]':
            accu_text = accu_text + text
            end = end_time
            if update_start:
                start = start_time
            if text[-1] != '.':
                update_start = False
                print("continue")
                print("total text: " + accu_text)
            else:
                print("find dot")
                print("total text: " + accu_text)
                df = df.append({'lecture': filename, 'start_time': start, 'end_time': end, 'text': accu_text}, ignore_index=True)
                accu_text = ''
                update_start = True
        else:
            update_start = True
    df.to_csv('./dataset/data.csv')
