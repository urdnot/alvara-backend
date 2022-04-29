from aiohttp import web
import multidict
import meta_generator
import artifacts_keeper
import smart_client
import token_state


class Server:
    COLLECTION_SETTINGS_PATH = "settings.json"
    ARTIFACTS_DIRECTORY = "artifacts/"
    HOST = "127.0.0.100"
    PORT = 8080
    KEEPALIVE_TIMEOUT = 60 #sec
    ETH_NODE_URL = "http://127.0.0.1:8545"
    SMART_CONTRACT_ADDRESS = "0xaD888d0Ade988EbEe74B8D4F39BF29a8d0fe8A8D"
    STATE_DIR = "state/"
    COLLECTION_SIZE = 10000
    DOMAIN = "alvara.io/"
    TOKEN_META_PATH = "token/"
    NORMAL_IMAGE_PATH = "image/"
    HIGH_IMAGE_PATH = "image/high/"

    def __init__(self):
        self.keeper = artifacts_keeper.ArtifactsKeeper(self.ARTIFACTS_DIRECTORY, self.COLLECTION_SETTINGS_PATH)
        self.smart = smart_client.SmartContract(self.ETH_NODE_URL, self.SMART_CONTRACT_ADDRESS)
        self.state = token_state.TokenState(self.ARTIFACTS_DIRECTORY + self.STATE_DIR, self.COLLECTION_SIZE)
        self.gen = meta_generator.MetaGenerator(self.keeper, self.state, self.smart, self.DOMAIN,
                                                self.NORMAL_IMAGE_PATH, self.HIGH_IMAGE_PATH)
        self.app = web.Application()
        self.app.add_routes([web.get("/" + self.TOKEN_META_PATH + "{id}", self.token_meta),
                             web.get("/" + self.NORMAL_IMAGE_PATH + "{id}", self.image)])

    def _convert_to_integer_id(self, str):
        if not str.isdigit():
            raise Exception("In token's meta and image request`id` must be integer number")
        id = int(str)
        if id > self.COLLECTION_SIZE or id < 1:
            raise Exception("In token's meta and image request`id` in range(1, {})".format(self.COLLECTION_SIZE + 1))
        return id

    async def token_meta(self, request):
        str_id = request.match_info.get('id')
        id = self._convert_to_integer_id(str_id)
        content = await self.gen.meta(id)
        return web.json_response(content)

    async def image(self, request):
        str_id = request.match_info.get('id')
        id = self._convert_to_integer_id(str_id)
        return web.Response(body=self.keeper.image_content(id),
                            headers=multidict.MultiDict({'Content-Type': 'image/png'}))


server = Server()

if __name__ == '__main__':
    web.run_app(server.app,
                host=server.HOST,
                port=server.PORT,
                keepalive_timeout=server.KEEPALIVE_TIMEOUT)
