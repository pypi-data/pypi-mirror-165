from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.models.data_nft import DataNFT
from ocean_lib.models.datatoken import Datatoken
from ocean_lib.web3_internal.constants import ZERO_ADDRESS
from ocean_lib.structures.file_objects import UrlFile
from ocean_lib.web3_internal.currency import from_wei

class Occean():
    
    def __init__(self,config,wallet_key:str,from_key:str) -> None:
        self.ocean = Ocean(config)
        print(f"Occean = {self.ocean.config.network_name}")
        self.wallet =self.getWallet(wallet_key)
        self.from_wallet = self.getWallet(from_key)
        print(f"Address of OCEAN token: {self.ocean.OCEAN_address}")
        self.OCEAN_token = self.ocean.OCEAN_token
        
    def publishNFTToken(self,name:str,symbol:str)->DataNFT:
        print(f"from_wallet = '{self.from_wallet.address}'")
        data_nft = self.ocean.create_data_nft(name, symbol, self.from_wallet)
        print(f"Created data NFT. Its address is {data_nft.address}")
        return data_nft
        
    def getWallet(self,test_key:str)->Wallet:
        wallet = Wallet(self.ocean.web3, test_key, self.ocean.config.block_confirmations, self.ocean.config.transaction_timeout)
        print(f"wallet.address = '{wallet.address}'")
        return wallet
    
    def createDataToken(self,data_nft:DataNFT,value:int)->Datatoken:
        datatoken = data_nft.create_datatoken("Datatoken 1", "DT1", from_wallet=self.from_wallet,minter = self.from_wallet.address)
        print(f"Created datatoken. Its address is {datatoken.address}")
        datatoken.mint(
        account_address=self.wallet.address,
        value=self.ocean.to_wei(value),
        from_wallet=self.from_wallet,
        )
        return datatoken
    
    def getDatatoken(self,token_address:str)->Datatoken:
        datatoken = self.ocean.get_datatoken(token_address)
        print(f"get datatoken = {datatoken.address}")
        return datatoken
    
    def getExchangeId(self,datatoken:Datatoken,amount:int,fixed_rate:int):
        assert self.ocean.web3.eth.get_balance(self.wallet.address) > 0, "need ganache ETH"

        self.OCEAN_token = self.ocean.OCEAN_token
        # Create exchange_id for a new exchange
        exchange_id = self.ocean.create_fixed_rate(
            datatoken=datatoken,
            base_token=self.OCEAN_token,
            amount=self.ocean.to_wei(amount),
            fixed_rate=self.ocean.to_wei(fixed_rate),
            from_wallet=self.from_wallet,
        )
        print(f"Exchange ID = {exchange_id}")
        return exchange_id
    
    def buy(self,datatoken:Datatoken,exchangeID,amount:int,max:int):
        # Approve tokens for Bob
        fixed_price_address = self.ocean.fixed_rate_exchange.address
        datatoken.approve(fixed_price_address, self.ocean.to_wei(4), self.wallet)
        self.OCEAN_token.approve(fixed_price_address, self.ocean.to_wei(4), self.wallet)

        tx_result = self.ocean.fixed_rate_exchange.buy_dt(
            exchange_id=exchangeID,
            datatoken_amount=self.ocean.to_wei(amount),
            max_base_token_amount=self.ocean.to_wei(max),
            consume_market_swap_fee_address=ZERO_ADDRESS,
            consume_market_swap_fee_amount=0,
            from_wallet=self.wallet,
        )
        assert tx_result, "failed buying datatokens at fixed rate for Bob"
        print(f"tx_result = {tx_result}")
        return tx_result


    def getBalance(self):
        OCEAN_balance_in_wei = self.OCEAN_token.balanceOf(self.wallet.address)
        
        OCEAN_balance_in_ether = from_wei(OCEAN_balance_in_wei)
        print(f"Balance: {OCEAN_balance_in_ether} OCEAN")
        if OCEAN_balance_in_wei == 0:
            print("WARNING: you don't have any OCEAN yet")
            
            
    def createDatasetExmple(self):
        # Specify metadata and services, using the Branin test dataset
        date_created = "2021-12-28T10:55:11Z"

        metadata = {
            "created": date_created,
            "updated": date_created,
            "description": "Branin dataset",
            "name": "Branin dataset",
            "type": "dataset",
            "author": "Trent",
            "license": "CC0: PublicDomain",
        }

        # ocean.py offers multiple file types, but a simple url file should be enough for this example

        url_file = UrlFile(
            url="https://raw.githubusercontent.com/trentmc/branin/main/branin.arff"
        )

        # Publish asset with services on-chain.
        # The download (access service) is automatically created, but you can explore other options as well
        asset = self.ocean.assets.create(
            metadata,
            self.from_wallet,
            [url_file],
            datatoken_templates=[1],
            datatoken_names=["Datatoken 1"],
            datatoken_symbols=["DT1"],
            datatoken_minters=[self.from_wallet.address],
            datatoken_fee_managers=[self.from_wallet.address],
            datatoken_publish_market_order_fee_addresses=[ZERO_ADDRESS],
            datatoken_publish_market_order_fee_tokens=[self.ocean.OCEAN_address],
            datatoken_publish_market_order_fee_amounts=[0],
            datatoken_bytess=[[b""]],
        )

        did = asset.did  # did contains the datatoken address
        print(f"did = '{did}'")

