import smart_client
import asyncio

NETWORK_NODE = "https://rinkeby.infura.io/v3/b7c623cd9b63446694c39630e8c5e18d"
SMART_CONTRACT_ADDRESS = "0x5E8aF42D3E9Ba51Aeb69F38C77896049642189fC"


async def main():
    alvara = smart_client.SmartContract(NETWORK_NODE, SMART_CONTRACT_ADDRESS)
    # print(await alvara.get_token_data(0))
    print(alvara.get_total_supply())


if __name__ == '__main__':
    asyncio.run(main())