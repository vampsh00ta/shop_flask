from config import app
class Handlers():
    def add_header(self,response):
        response.headers['Server'] = ''
        return response