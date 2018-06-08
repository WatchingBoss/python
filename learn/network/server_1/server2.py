import io
import socket
import sys

class wsgiServer(object):
    addressFamily = socket.AF_INET
    socketType = socket.SOCK_STREAM
    requestQueueSize = 2

    def __init__(self, serverAddress):
        # Create a listenin socket
        self.lSocket = lSocket = socket.socket(self.addressFamily, self.socketType)
        # Allow to reuse the same address
        lSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind
        lSocket.bind(serverAddress)
        # Activate
        lSocket.listen(self.requestQueueSize)
        # Get server host name and post
        host, port = "127.0.0.1", 12000 #self.lSocket.getsockname()[:2]
        self.serverName = socket.getfqdn(host)
        self.serverPort = port
        print ("\n{0};\n{1};\n{2};\n{3};\n".format(host, port, self.serverName, self.serverPort))
        # Return headers set by Web framework/app
        self.headersSet = []

    def set_app(self, app):
        self.app = app

    def server_work(self):
        lSocket = self.lSocket

        while True:
            # New client connection
            self.clientConnect, clientAddr = lSocket.accept()
            # Handle 1 request and close connection; wait for another one
            self.handle_request()

    def handle_request(self):
        self.requestData = requestData = self.clientConnect.recv(1024)
        # Print request
        print (''.join('< {line}\n'.format(line=line)
                       for line in requestData.splitlines()))
        self.parse_request(requestData)
        # Construct environment dictionary using request data
        environment = self.get_environment()
        # Call app and return result aka HTTP response body
        result = self.app(environment, self.start_response)
        # Construct and send the response
        self.finish_response(result)

    def parse_request(self, text):
        requestLine = text.splitlines()[0]
        requestLine = requestLine.rstrip('\r\n'.encode())
        # Break down the request into lines
        (self.requestMethod, self.path, self.requestVersion) = requestLine.split()

    def get_environment(self):
        environment = {}
        # Emphasize the required vars and their values
        # Requires WSGI vars
        environment['wsgi.version'] = (1, 0)
        environment['wsgi.url_scheme'] = "http"
        environment['wsgi.input'] = io.BytesIO(self.requestData)
        environment['wsgi.errors'] = sys.stderr
        environment['wsgi.multithread'] = False
        environment['wsgi.multiprocess'] = False
        environment['wsgi.run_once'] = False
        # Required CGI vars
        environment['wsgi.REQUEST_METHOD'] = self.requestMethod
        environment['wsgi.PATH_INFO'] = self.path
        environment['wsgi.SERVER_NAME'] = self.serverName
        environment['wsgi.SERVER_PORT'] = str(self.serverPort)

        return environment

    def start_response(self, status, responseHeaders, excInfo=None):
        # Add necessary server headers
        serverHeaders = [("Date", "Today"), ("Server", "WSGIserver")]

        self.headersSet = [status, responseHeaders + serverHeaders]

    def finish_response(self, result):
        try:
            status, responseHeaders = self.headersSet
            response = ("HTTP/1.1 [status]\r\n".format(status=status))
            for header in responseHeaders:
                response += "{0}: {1}\r\n".format(*header)
                response += "\r\n"
            for data in result:
                response += data
            print("".join("> {line}\n".format(line=line)
                          for line in response.splitlines()))
            self.clientConnect.sendall(response.encode())
        finally:
            self.clientConnect.close()

SERVER_ADDRESS = (HOST, PORT) = '', 12000

def make_server(serverAddress, app):
    server = wsgiServer(serverAddress)
    server.set_app(app)
    return server

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Provide object as module:callable")
    appPath = sys.argv[1]
    module, app = appPath.split(":")
    module = __import__(module)
    app = getattr(module, app)
    httpd = make_server(SERVER_ADDRESS, app)
    
    print("wsgiServer: HTTP on port {port}\n".format(port=PORT))
    httpd.server_work()

