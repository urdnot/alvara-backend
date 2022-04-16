from aiohttp import web
import multidict
import meta_generator
import artifacts_keeper
import smart_client


class Server:
    SETTINGS_PATH = "settings.json"
    ARTIFACTS_DIRECTORY = "artifacts/"
    HOST = "127.0.0.1"
    PORT = 8080
    ETH_NODE_URL = "http://127.0.0.1:8545"
    SMART_CONTRACT_ADDRESS = "0xCfEB869F69431e42cdB54A4F4f105C19C080A601"

    def __init__(self):
        self.keeper = artifacts_keeper.ArtifactsKeeper(self.ARTIFACTS_DIRECTORY, self.SETTINGS_PATH)
        self.smart = smart_client.SmartContract(self.ETH_NODE_URL, self.SMART_CONTRACT_ADDRESS)
        self.gen = meta_generator.MetaGenerator(self.keeper)
        self.app = web.Application()
        self.app.add_routes([web.get('/', self.default),
                             web.get('/token/{id}', self.token_meta),
                             web.get('/image/{id}', self.image)])

    async def default(self, request):
        return web.json_response({'error': 'invalid request'})

    async def token_meta(self, request):
        id = request.match_info.get('id')
        return web.json_response(self.gen.meta(id))

    async def image(self, request):
        id = request.match_info.get('id')
        return web.Response(body=self.keeper.image_content(id),
                            headers=multidict.MultiDict({'Content-Type': 'image/png'}))


server = Server()

if __name__ == '__main__':
    web.run_app(server.app, host=server.HOST, port=server.PORT)