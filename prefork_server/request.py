from urllib.parse import urlparse, unquote

class Request:
    def __init__(self, raw_request):
        self.raw_request = raw_request.decode()                     # переводим байт-код в строку
        self.method = (self.raw_request.split(' '))[0]
        self.path = self.make_path()

    def make_path(self):
        # на случай обработки пустого url
        try:
            url = (self.raw_request.split(' '))[1]
        except BaseException as e:
            return 0
        #url = (self.raw_request.split(' '))[1]
        raw_path = urlparse(url).path                               # Парсим url и достаем path
        path = unquote(raw_path)                                    # %xx => x
        return path
