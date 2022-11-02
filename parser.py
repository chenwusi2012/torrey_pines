import webvtt
import pandas as pd

if __name__ == '__main__':
    start = ''
    end = ''
    total_text = ''
    df = pd.DataFrame(columns=['lecture', 'start_time', 'end_time', 'text'])
    filename = 'Lesson 1.2 Text Access.vtt'
    captions = webvtt.read('./subtitles/' + filename)
    for idx, caption in enumerate(captions):
        start_time = caption.start
        end_time = caption.end
        text = caption.text
        text = text.replace('\n', ' ')
        if text != '[SOUND]' or text != '[MUSIC]':
            if text[-1] != '.':
                total_text = total_text + text
            else:
                df = df.append({'lecture': filename, 'start_time': start_time, 'end_time': end_time, 'text': total_text}, ignore_index=True)
                total_text = ''
    df.to_csv('./dataset/data.csv')
    print(df.head(3))
