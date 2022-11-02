def convert_time(time_stamp):
    values = time_stamp.split(':')
    second = int(values[0]) * 3600 + int(values[1]) * 60 + int(values[2])
    return second


if __name__ == '__main__':
    print(convert_time("00:01:32"))
