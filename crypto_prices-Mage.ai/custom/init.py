from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from mage_ai.data_preparation.variable_manager import set_global_variable

@custom
def getInterval(*args, **kwargs):
    ''' set global variables '''
    pipeline_uuid = kwargs.get("pipeline_uuid")

    # Current Interval
    END_DATETIME = datetime.utcnow() #- relativedelta(days=1)
    END_DATETIME = datetime(END_DATETIME.year, END_DATETIME.month, END_DATETIME.day, END_DATETIME.hour)
    START_DATETIME = END_DATETIME - relativedelta(minutes=10)
    set_global_variable(pipeline_uuid, "END_DATETIME", END_DATETIME)
    set_global_variable(pipeline_uuid, "START_DATETIME", START_DATETIME)
    
    # The List of cryptocurrencies
    coins = {"AAVE": "Aave", "BTC": "Bitcoin", "ADA": "Cardano", "LINK": "Chainlink", 
            "DOGE": "Dogecoin", "EOS": "EOS", "ETH": "Ethereum", "LTC": "Litecoin", 
            "DOT": "Polkadot", "XLM": "Stellar", "USDT": "Tether", "UNI": "Uniswap", 
            "USDC": "USD-Coin", "XRP": "XRP"}
    coin_symbols = list(coins.keys())
    coin_names = list(coins.values())

    set_global_variable(pipeline_uuid, "coins", coins)
    set_global_variable(pipeline_uuid, "coin_symbols", coin_symbols)
    set_global_variable(pipeline_uuid, "coin_names", coin_names)