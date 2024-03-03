import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    df.reset_index(inplace=True)
    df.rename(columns={"index": "ID"}, inplace=True)

    # Feature Engineering
    df["Date"] = kwargs.get("END_DATETIME").strftime('%Y-%m-%d')
    df["Time"] = kwargs.get("END_DATETIME").strftime('%H:%M:%S')
    df = df[['ID', 'Date', 'Time', 'MarketCap', 'Volume']]
    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
