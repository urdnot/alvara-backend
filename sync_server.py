from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import meta_generator
import artifacts_keeper
import smart_client

SETTINGS_PATH = "settings.json"
ARTIFACTS_DIRECTORY = "artifacts/"
ETH_NODE_URL = "http://127.0.0.1:8545"
SMART_CONTRACT_ADDRESS = "0xCfEB869F69431e42cdB54A4F4f105C19C080A601"


class Server(BaseHTTPRequestHandler):
    token_rx = re.compile("^/token/[1-9][0-9]*$")
    normal_image_rx = re.compile("^/image/normal/[1-9][0-9]*$")
    keeper = artifacts_keeper.ArtifactsKeeper(ARTIFACTS_DIRECTORY, SETTINGS_PATH)
    smart = smart_client.SmartContract(ETH_NODE_URL, SMART_CONTRACT_ADDRESS)
    gen = meta_generator.MetaGenerator(keeper)

    def _set_json_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _set_png_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()

    def _str_to_bytes(self, str):
        return bytes(str, 'utf-8')

    def do_HEAD(self):
        self._set_json_headers()

    # GET
    def do_GET(self):
        if self.token_rx.match(self.path):
            self._set_json_headers()
            token_id = int(self.path[7:]) # len("/token/")
            self.wfile.write(self._str_to_bytes(json.dumps(self.gen.meta(token_id))))
        elif self.normal_image_rx.match(self.path):
            self._set_png_headers()
            token_id = int(self.path[7:])  # len("/image/")
            self.wfile.write(self.keeper.image_content(token_id))
        else:
            self._set_json_headers()
            self.wfile.write(self._str_to_bytes(json.dumps({'error': 'invalid request'})))


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    run()