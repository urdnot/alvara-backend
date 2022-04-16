import smart_client


ETH_NODE_URL = "http://127.0.0.1:8545"
SMART_CONTRACT_ADDRESS = "0xCfEB869F69431e42cdB54A4F4f105C19C080A601"


def main():
    alvara = smart_client.SmartContract(ETH_NODE_URL, SMART_CONTRACT_ADDRESS)
    print(alvara.get_token_data())


if __name__ == '__main__':
    main()