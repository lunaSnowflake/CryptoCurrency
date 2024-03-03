from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import logging

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(df, *args, **kwargs):
    # format in proper datetime
    df.rename(columns={'Timestamp': 'Datetime'}, inplace=True)
    df['Datetime'] = pd.to_datetime(df['Datetime']).dt.round('H')

    # format data
    df.reset_index(drop=True, inplace=True)
    df[['Open', 'High', 'Low', 'Close']] = round(df[['Open', 'High', 'Low', 'Close']],4)

    # feature eng.
    df['Date'] = pd.to_datetime(df['Datetime']).dt.strftime('%Y-%m-%d')
    df['Time'] = pd.to_datetime(df['Datetime']).dt.strftime('%H:%M:%S')
    df.drop('Datetime', axis=1, inplace=True)
    
    df = df[['ID', 'Date', 'Time', 'Open', 'High', 'Low', 'Close']]

    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
