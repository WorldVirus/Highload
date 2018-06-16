from urllib.parse import urlparse, unquote

class Request:
    def __init__(self, raw_request):
        self.raw_request = raw_request.decode()                     
        self.method = (self.raw_request.split(' '))[0]
        self.path = self.make_path()

    def make_path(self):
        
        try:
            url = (self.raw_request.split(' '))[1]
        except BaseException as e:
            return 0
        
        raw_path = urlparse(url).path                              
        path = unquote(raw_path)                                   
        return path
