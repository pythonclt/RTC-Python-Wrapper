
from threading import Thread
import urllib2

from wsgiref.simple_server import make_server

class MockServer(Thread):
    """
    Simple mock server which might be useful so don't have to depend
    on internet access and data in the datasource
    """
    host = 'localhost'
    port = 9876
   
    @classmethod
    def handle(self, app):
        """
        Most common testing case for handling a single request.
        """
        s = MockServer()
        s.__create(app)
        s.start()
    
    def __init__(self):
        Thread.__init__(self)
        self.httpd = None

    def __create(self, app):
        """
        Common for initializing the server
        """
        if self.httpd is None:
            self.httpd = make_server(self.host, self.port, app)
        else:
            self.httpd.set_app(app)
    def serve(self, app):
        """
        Built in server that will run until it is stopped.
        """
        self.__create(app)


    def run(self):
        self.httpd.handle_request()

