import smart_client


ETH_NODE_URL = "http://127.0.0.1:8545"
SMART_CONTRACT_ADDRESS = "0xb09bCc172050fBd4562da8b229Cf3E45Dc3045A6"


def main():
    alvara = smart_client.SmartContract(ETH_NODE_URL, SMART_CONTRACT_ADDRESS)
    print(alvara.get_token_data(0).call())


if __name__ == '__main__':
    main()