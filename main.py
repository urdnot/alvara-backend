from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import meta_generator as gen


class Server(BaseHTTPRequestHandler):
    token_rx = re.compile("^/token/[1-9][0-9]*$")

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _str_to_bytes(self, str):
        return bytes(str, 'utf-8')

    def do_HEAD(self):
        self._set_headers()

    # GET
    def do_GET(self):
        self._set_headers()
        if self.token_rx.match(self.path):
            num = int(self.path[7:]) # len("/token/")
            self.wfile.write(self._str_to_bytes(json.dumps(gen.meta(num))))
        else:
            self.wfile.write(self._str_to_bytes(json.dumps({'error': 'invalid request'})))


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    run()