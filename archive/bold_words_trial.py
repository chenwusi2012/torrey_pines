TEXT = "[SOUND] This lecture) is about the feedback in the language modeling approach. In this lectures,"

QUERY = "Feedback lecture"


def bold_words(text, query):
    print(text)
    mark = [',', '.', ';', ':', '?', ')', '(']
    words = text.split(' ')
    query = query.lower()
    terms = query.split(' ')
    for idx, word in enumerate(words):
        if word[-1] in mark:
            end_character = word[-1]
            word = word[0:-1]
            if word.lower() in terms:
                words[idx] = "<b>" + word + "</b>" + end_character
            else:
                words[idx] = word + end_character
        else:
            if word.lower() in terms:
                words[idx] = "<b>" + word + "</b>"
            else:
                words[idx] = word
    return ' '.join(words)


if __name__ == '__main__':
    print(bold_words(TEXT, QUERY))
