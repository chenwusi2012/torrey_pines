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
    %for segment in result:
    <p>
        {{ segment['index'] }}<br>
        <b>{{ segment['lecture'] }}</b><br>
        {{ segment['start_time'] }} - {{ segment['end_time'] }}<br>
        {{ segment['text'] }}<br>
        <a href="{{ segment['link'] }}"> Go to this segment</a>
    </p>
    %end
</body>
</html>