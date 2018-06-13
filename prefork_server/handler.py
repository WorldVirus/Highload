import os

from request import Request
from http_const import ResponseCode, CONTENT_TYPES, DEFAULT_PAGE
from response import Response

class Handler:
    def __init__(self, root, request):
        self.root = root
        self.request = Request(request)

    def get_response(self):
        if self.request.method in ['GET', 'HEAD']:
            response = self.make_response()
        else:
            response = Response(ResponseCode.NOT_ALLOWED)
        return response.create_response()

    def get_content_type(self, path):
        type = path.split('.')[-1]
        return CONTENT_TYPES.get(type, '')

    def make_response(self):
        response = Response(ResponseCode.NOT_FOUND)
        real_path = os.path.normpath(self.root + self.request.path)       # нормализую путь

        # проверка на выход из root
        if (os.path.commonpath([real_path, self.root])) != self.root:     # commonpath - вернет общий путь
            return response

        if os.path.isfile(os.path.join(real_path, DEFAULT_PAGE)):
            real_path = os.path.join(real_path, DEFAULT_PAGE)
        elif os.path.exists(real_path):                                         # директория||файл существует
            response.code = ResponseCode.FORBIDDEN
        else:                                                                   # директория||файл не существует
            return response

        try:
            file = open(real_path, 'rb')
            content = file.read()
            if self.request.method == 'GET':
                response.content = content
                response.content_type = self.get_content_type(real_path)
            response.content_length = len(content)
            response.code = ResponseCode.OK
            file.close()
        except IOError as e:
            print("Error in path: " + real_path)                                       # 403 (см. http_const)

        return response
