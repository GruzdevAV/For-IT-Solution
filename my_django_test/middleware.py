#https://stackoverflow.com/questions/65365235/django-how-can-i-get-the-request-before-the-main-urls-py

import logging, sqlite3, time
from django.core.handlers.wsgi import WSGIRequest

logger = logging.getLogger('name_of_my_logger')

sql = "INSERT INTO requests (date_time, headers, body) VALUES (?,?,?)"

def logging_middleware(get_response):
    # One-time configuration and initialization.
    def middleware(request: WSGIRequest):
        logger.info(request.build_absolute_uri())
        response = get_response(request)
        print(request.headers)
        print(request.headers.items())
        insert_data = (time.time_ns(), str(request.headers), request.body)
        with sqlite3.connect("db.sqlite3") as con:
            cursor = con.cursor()
            cursor.execute(sql, insert_data)
        return response
    return middleware
