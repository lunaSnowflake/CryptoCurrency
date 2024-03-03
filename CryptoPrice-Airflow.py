# Import Libraries
import requests
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import mysql.connector
import logging
from decouple import config
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# load sql endpoint credentials
DB_HOST=config("DB_HOST")
DB_PORT=config("DB_PORT")
DB_USER=config("DB_USER")
DB_PASSWORD=config("DB_PASSWORD")
DB_NAME=config("DB_NAME")

# The List of cryptocurrencies
coins = {"AAVE": "Aave", "BTC": "Bitcoin", "ADA": "Cardano", "LINK": "Chainlink", "DOGE": "Dogecoin", "EOS": "EOS", "ETH": "Ethereum", 
         "LTC": "Litecoin", "DOT": "Polkadot", "XLM": "Stellar", "USDT": "Tether", "UNI": "Uniswap", "USDC": "USD-Coin", "XRP": "XRP"}
coin_symbols = list(coins.keys())
coin_names = list(coins.values())

# Global Variables
START_DATETIME = datetime.utcnow()
END_DATETIME = datetime.utcnow()
OHLC_DF = pd.DataFrame()
MCAP_VOL_DF = pd.DataFrame()
CONN = ""
CURSOR = ""

def connectSQL():
    ''' Connect to the SQL endpoint '''
    global CONN, CURSOR

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
    
def disconnectSQL():
    ''' Disconnect to the SQL endpoint '''
    global CONN, CURSOR
    if CONN.is_connected():
        CURSOR.close()
        CONN.close()
        logging.info("Connection closed")

def getOHLC(verbose=False):
    ''' Get OHLC metrics '''
    global START_DATETIME, END_DATETIME, OHLC_DF
    OHLC_DF = pd.DataFrame()
    start_datetime, end_datetime = START_DATETIME.strftime("%Y-%m-%dT%H:%M"), END_DATETIME.strftime("%Y-%m-%dT%H:%M")
    for i, coin in enumerate(coin_symbols):
        url = "https://production.api.coindesk.com/v2/price/values/{}?start_date={}&end_date={}&ohlc=true".format(coin, start_datetime, end_datetime)
        if verbose: logging.info("Requesting...:", url)

        # request
        try:
            temp_data = requests.get(url).json()

            if temp_data.get("statusCode") != 200:
                raise ValueError(f'{temp_data.get("statusCode")}: {temp_data.get("message")}')

            df = pd.DataFrame(temp_data['data']['entries'], columns=['Timestamp', 'Open', 'High', 'Low', 'Close'])

            # format in proper datetime
            df['Timestamp'] = df['Timestamp'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime("%Y-%m-%d %H:%M:%S"))
            df.rename(columns={'Timestamp': 'Datetime'}, inplace=True)
            df['Datetime'] = pd.to_datetime(df['Datetime']).dt.round('H')

            # format data
            df.sort_values('Datetime', ascending=False, inplace=True)
            df.drop_duplicates('Datetime', keep='first', inplace=True)
            df.reset_index(drop=True, inplace=True)
            df[['Open', 'High', 'Low', 'Close']] = round(df[['Open', 'High', 'Low', 'Close']],2)

            # Take the max datetime record only (just in case)
            df = df.head(1).copy()

            # feature eng.
            df['Date'] = pd.to_datetime(df['Datetime']).dt.strftime('%Y-%m-%d')
            df['Time'] = pd.to_datetime(df['Datetime']).dt.strftime('%H:%M:%S')
            df.drop('Datetime', axis=1, inplace=True)
            df['ID'] = i+1

            df = df[['ID', 'Date', 'Time', 'Open', 'High', 'Low', 'Close']]

            if verbose:
                logging.info("Total records found:", df.shape)
                logging.info("Data in the time interval of:", temp_data['data']['interval'])

        except Exception as err:
            logging.error(err)
            df = None

        OHLC_DF = pd.concat((OHLC_DF, df))

def getMCapVol():
    ''' Get Market Cap and Volume '''
    global MCAP_VOL_DF
    cryptoMetrics = {"MarketCap": {}, "Volume": {}}
    for i, coin in enumerate(coins.values()):
        r = requests.get(f'https://coinmarketcap.com/currencies/{coin}/', timeout=5)
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        metrics = soup.find_all(class_="sc-16891c57-0 fRWxhs base-text")
        metrics = (metrics[0].text, metrics[1].text)
        cryptoMetrics["MarketCap"][i+1] = int(metrics[0][metrics[0].find("$")+1:].replace(",", "")) # MarketCap
        cryptoMetrics["Volume"][i+1] = int(metrics[1][metrics[1].find("$")+1:].replace(",", "")) # Volume
    MCAP_VOL_DF = pd.DataFrame(cryptoMetrics)

def getInterval():
    ''' Current Interval '''
    global START_DATETIME, END_DATETIME
    END_DATETIME = datetime.utcnow() #- relativedelta(days=1)
    END_DATETIME = datetime(END_DATETIME.year, END_DATETIME.month, END_DATETIME.day, END_DATETIME.hour)
    START_DATETIME = END_DATETIME - relativedelta(minutes=10)
    logging.info("End:", END_DATETIME)
    logging.info("Start:", START_DATETIME)


def insertRDS():
    ''' Insert a record into RDS '''
    global CONN, CURSOR
    try:
        logging.info(f"Inserting in {len(OHLC_DF)} records into OHLC_DF...")
        for row in OHLC_DF.iterrows():
            insert_query = '''INSERT INTO prices VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            record_to_insert = tuple(row[1].values)
            CURSOR.execute(insert_query, record_to_insert)

        logging.info(f"Inserting in {len(MCAP_VOL_DF)} records into MCAP_VOL_DF...")
        for row in MCAP_VOL_DF.iterrows():
            insert_query = '''INSERT INTO mcap_vol VALUES (%s, %s, %s, %s, %s)'''
            record_to_insert = (row[0], END_DATETIME.date().strftime('%Y-%m-%d'), END_DATETIME.time().strftime('%H:%M:%S'), int(row[1].get("MarketCap")), int(row[1].get("Volume")))
            CURSOR.execute(insert_query, record_to_insert)
        CONN.commit()
        logging.info("Records inserted successfully")
    except Exception as err:
        logging.fatal(err)


# Define the default arguments for the DAG
default_args = {
    'owner': 'sain',
    'depends_on_past': False,
    'start_date': datetime.utcnow().replace(minute=0, second=0, microsecond=0), #datetime(2023, 9, 14, 10, 0),
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}

# Instantiate the DAG
'''
Note: The dag will start running at first_run_time = start_date + schedule_interval, 
        if current time > first_run_time the dag will start immediately.
'''
with DAG(
    'crypto_hourly_dag',
    default_args=default_args,
    schedule_interval="@hourly" #timedelta(hours=1),  # Set the schedule to run every hour
) as dag:

    # Tasks
    connectSQL_ = PythonOperator(task_id='run_connectSQL', python_callable=connectSQL,)
    getInterval_ = PythonOperator(task_id='run_getInterval', python_callable=getInterval)
    getOHLC_ = PythonOperator(task_id='run_getOHLC', python_callable=getOHLC)
    getMCapVol_ = PythonOperator(task_id='run_getMCapVol', python_callable=getMCapVol)
    insertRDS_ = PythonOperator(task_id='run_insertRDS', python_callable=insertRDS)
    disconnectSQL_ = PythonOperator(task_id='run_disconnectSQL', python_callable=disconnectSQL)

connectSQL_ >> getInterval_ >> getOHLC_ >> getMCapVol_ >> insertRDS_ >> disconnectSQL_
