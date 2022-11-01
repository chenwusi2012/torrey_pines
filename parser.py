import webvtt

if __name__ == '__main__':
    captions = webvtt.read('./subtitles/Lesson 1.2 Text Access.vtt')
    print(type(captions))

