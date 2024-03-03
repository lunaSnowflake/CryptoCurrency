import requests
import pandas as pd
from bs4 import BeautifulSoup

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def getMCapVol(data, *args, **kwargs):
    ''' Get Market Cap and Volume '''
    END_DATETIME, START_DATETIME = kwargs["END_DATETIME"], kwargs["START_DATETIME"]
    start_datetime, end_datetime = START_DATETIME.strftime("%Y-%m-%dT%H:%M"), END_DATETIME.strftime("%Y-%m-%dT%H:%M")

    cryptoMetrics = {"MarketCap": {}, "Volume": {}}
    for i, coin in enumerate(kwargs["coin_names"]):
        # request page
        r = requests.get(f'https://coinmarketcap.com/currencies/{coin}/', timeout=5)
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')

        # extract MarketCap and Volume
        metrics = soup.find_all(class_="sc-16891c57-0 fRWxhs base-text")
        metrics = (metrics[0].text, metrics[1].text)
        cryptoMetrics["MarketCap"][i+1] = int(metrics[0][metrics[0].find("$")+1:].replace(",", "")) # MarketCap
        cryptoMetrics["Volume"][i+1] = int(metrics[1][metrics[1].find("$")+1:].replace(",", "")) # Volume

    MCAP_VOL_DF = pd.DataFrame(cryptoMetrics)
    
    return MCAP_VOL_DF

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
