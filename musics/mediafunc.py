import datetime
import uuid


def add_songs(instance, filename):
    mime = filename.split('.')[-1]
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    name = uuid.uuid4().hex
    return f"media/songs/{year}/{month}/{day}/{hour}/{name}.{mime}"


def add_images(instance, filename):
    mime = filename.split('.')[-1]
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    name = uuid.uuid4().hex
    return f"media/images/{year}/{month}/{day}/{hour}/{name}.{mime}"
