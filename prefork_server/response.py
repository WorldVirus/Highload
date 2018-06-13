from datetime import datetime

import http_const
import config
from http_const import ResponseCode


class Response:
    def __init__(self, code):
        self.code = code
        self.content = b''
        self.content_length = 0
        self.content_type = ''

    def create_response(self):
        if self.code == ResponseCode.OK:
            response = self.response_ok()
        else:
            response = self.response_fail()
        return response

    def response_ok(self):
        response = ('HTTP/{http_version} {http_status}\r\n'
                    'Server: {server_name}\r\n'
                    'Date: {date}\r\n'
                    'Connection: Closed\r\n'
                    'Content-Length: {content_length}\r\n'
                    'Content-Type: {content_type}\r\n\r\n') \
            .format(http_version=http_const.HTTP_VERSION,
                    http_status=http_const.RESPONSE_STATUS.get(self.code.value, ''),
                    server_name=config.SERVER_NAME,
                    date=self.get_now_date(http_const.HTTP_DATE_FORMAT),
                    content_length=self.content_length,
                    content_type=self.content_type)
        return response.encode() + self.content

    def get_now_date(self, data_format):
        return datetime.utcnow().strftime(data_format)

    def response_fail(self):
        response = ('HTTP/{http_version} {http_status}\r\n'
                    'Server: {server_name}\r\n'
                    'Date: {date}\r\n'
                    'Connection: Closed\r\n\r\n') \
                    .format(http_version=http_const.HTTP_VERSION,
                            http_status=http_const.RESPONSE_STATUS.get(self.code.value, ''),
                            server_name=config.SERVER_NAME,
                            date=self.get_now_date(http_const.HTTP_DATE_FORMAT))
        return response.encode()
