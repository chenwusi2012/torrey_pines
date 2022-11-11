<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CS410 Video Segment Search</title>
</head>
<body>
    <h2>CS410 Video Segment Search</h2>
    <form action="/search" method="post">
        <input  name="query" type="text" value="{{ query }}" size="50">
        <button type="submit">Search</button>
    </form>
    <div><a href="/"> Return to home page</a></div>
    <p>Video segments related to <b>{{ query }}</b> ({{ time_delta}} seconds):</p>
    %if is_empty == True:
    <h3 style="text-align:center"><br>No video segment related to "{{ query }}"</h3>
    %else:
    %for segment in result:
    <p>
        {{ segment['index'] }}<br>
        <b>{{ segment['lecture'] }}</b><br>
        {{ segment['start_time'] }} - {{ segment['end_time'] }}<br>
        {{ segment['text'] }}<br>
        <p>
        %mark = [',', '.', ';', ':', '?', ')', '(']
        %words = segment['text'].split(' ')
        %query = query.lower()
        %terms = query.split(' ')
        %for idx, word in enumerate(words):
            %if word[-1] in mark:
                %end_character = word[-1]
                %word = word[0:-1]
                %if word.lower() in terms:
                    <mark>{{ word }}</mark>{{ end_character }}
                %else:
                    {{ word }}{{ end_character }}
                %end
            %else:
                %if word.lower() in terms:
                    <mark>{{ word }}</mark>
                %else:
                    {{ word }}
                %end
            %end
        %end
        </p>
        <a href="{{ segment['segment_link'] }}"> Go to this segment ({{ segment['start_time'] }} - {{ segment['end_time'] }})</a><br>
        <a href="{{ segment['lecture_link'] }}"> Go to this lecture ({{ segment['lecture'] }})</a>
    </p>
    %end
    %end
</body>
</html>