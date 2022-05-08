from aiohttp import web
import multidict
import meta_generator
import artifacts_keeper
import smart_client
import token_state


class Server:
    COLLECTION_SETTINGS_PATH = "settings.json"
    ARTIFACTS_DIRECTORY = "artifacts/"
    HOST = "127.0.0.1"
    PORT = 8080
    KEEPALIVE_TIMEOUT = 60 #sec'
    # NETWORK_NODE = "http://127.0.0.1:8545"                                            # Local
    # SMART_CONTRACT_ADDRESS = "0x4E20EE2C494d40aC0c04c8730D92EC701d7d7f40"             # Local
    NETWORK_NODE = "https://rinkeby.infura.io/v3/b7c623cd9b63446694c39630e8c5e18d"      # Rinkeby testnet
    SMART_CONTRACT_ADDRESS = "0x5E8aF42D3E9Ba51Aeb69F38C77896049642189fC"               # Rinkeby testnet
    STATE_DIR = "state/"
    COLLECTION_SIZE = 10000
    DOMAIN = "https://2cf1-188-122-0-10.eu.ngrok.io/"                                   # Static domain
    TOKEN_META_PATH = "token/"
    IMAGE_PATH = "image/"
    EXTERNAL_PATH = "external/"

    def __init__(self):
        self.keeper = artifacts_keeper.ArtifactsKeeper(self.ARTIFACTS_DIRECTORY, self.COLLECTION_SETTINGS_PATH)
        self.smart = smart_client.SmartContract(self.NETWORK_NODE, self.SMART_CONTRACT_ADDRESS)
        self.state = token_state.TokenState(self.ARTIFACTS_DIRECTORY + self.STATE_DIR, self.COLLECTION_SIZE)
        self.gen = meta_generator.MetaGenerator(self.keeper, self.state, self.smart, self.DOMAIN,
                                                self.IMAGE_PATH, self.EXTERNAL_PATH)
        self.app = web.Application()
        self.app.add_routes([web.get("/" + self.TOKEN_META_PATH + "{id}", self.token_meta),
                             web.get("/" + self.IMAGE_PATH + "{id}", self.image),
                             web.get("/" + self.EXTERNAL_PATH + "{id}", self.external)])

    def _convert_to_integer_id(self, str):
        if not str.isdigit():
            raise Exception("In token's meta and image request`id` must be integer number")
        id = int(str)
        if id >= self.COLLECTION_SIZE or id < 0:
            raise Exception("In token's meta and image request`id` in range(0, {})".format(self.COLLECTION_SIZE))
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

    async def external(self, request):
        str_id = request.match_info.get('id')
        id = self._convert_to_integer_id(str_id)
        return web.Response(body=self.keeper.external_content(id),
                            headers=multidict.MultiDict({'Content-Type': 'image/png'}))


server = Server()

if __name__ == '__main__':
    web.run_app(server.app,
                host=server.HOST,
                port=server.PORT,
                keepalive_timeout=server.KEEPALIVE_TIMEOUT)
