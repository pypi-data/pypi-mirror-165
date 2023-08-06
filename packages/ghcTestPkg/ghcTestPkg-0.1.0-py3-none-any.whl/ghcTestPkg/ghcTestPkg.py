import datetime
def add_timestamp(data):
    timestamp = "<{0}>".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return timestamp + " " + data + "ghcTest"