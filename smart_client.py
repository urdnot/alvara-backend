from web3 import Web3
import json


class SmartContract:
    def __init__(self, node_url, address):
        self.url = node_url
        self.address = address
        self.w3 = Web3(Web3.HTTPProvider(node_url))

        with open("AlvaraStorage.json") as f:
            info_json = json.load(f)
        self.abi = info_json["abi"]

        self.alvara = self.w3.eth.contract(address=self.address, abi=self.abi)

    def get_token_data(self, token_id):
        return self.alvara.functions.getData(token_id).call()

    def get_total_supply(self):
        return self.alvara.functions.totalSupply().call()
