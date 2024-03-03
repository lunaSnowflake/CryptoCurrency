from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import pandas as pd
import logging

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def getOHLC(data, *args, **kwargs):
    ''' Get OHLC metrics '''
    verbose = False
    END_DATETIME, START_DATETIME = kwargs["END_DATETIME"], kwargs["START_DATETIME"]
    OHLC_DF = pd.DataFrame()
    start_datetime, end_datetime = START_DATETIME.strftime("%Y-%m-%dT%H:%M"), END_DATETIME.strftime("%Y-%m-%dT%H:%M")
    for i, coin in enumerate(kwargs["coin_symbols"]):
        url = "https://production.api.coindesk.com/v2/price/values/{}?start_date={}&end_date={}&ohlc=true".format(coin, start_datetime, end_datetime)
        if verbose: print("Requesting...:", url)

        # request
        try:
            temp_data = requests.get(url).json()

            if temp_data.get("statusCode") != 200:
                raise ValueError(f'{temp_data.get("statusCode")}: {temp_data.get("message")}')

            df = pd.DataFrame(temp_data['data']['entries'], columns=['Timestamp', 'Open', 'High', 'Low', 'Close'])
            
            df['Timestamp'] = df['Timestamp'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime("%Y-%m-%d %H:%M:%S"))
            df.sort_values('Timestamp', ascending=False, inplace=True)
            df = df.head(1).copy()
            df['ID'] = i+1
            
            if verbose:
                print("Total records found:", df.shape)
                print("Data in the time interval of:", temp_data['data']['interval'])

        except Exception as err:
            logging.error(err)
            df = None

        OHLC_DF = pd.concat((OHLC_DF, df))
    
    return OHLC_DF

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
