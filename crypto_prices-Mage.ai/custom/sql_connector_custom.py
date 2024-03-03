import logging
if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import mysql.connector
DB_HOST="crypto-price.cjwpzpzmpx8w.ap-northeast-1.rds.amazonaws.com"
DB_PORT=3306
DB_USER="admin"
DB_PASSWORD="cryptoniki67"
DB_NAME="CryptoPriceDB"

# connect
try:
    CONN = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    CURSOR = CONN.cursor()
    logging.info("Connected to the database!")
except mysql.connector.Error as error:
    logging.error(error)

# disconnect
CURSOR.close()
CONN.close()

@custom
def transform_custom(data, *args, **kwargs):
    """
    Args:
        data: The output from the upstream parent block (if applicable)
        args: The output from any additional upstream blocks

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
