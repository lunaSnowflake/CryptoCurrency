# CryptoCurrency

This repository showcases the development of an end-to-end cryptocurrency dashboard orchestrated on AWS infrastructure using MageAI. The dashboard captures real-time OHLC (Open, High, Low, Close) data via an API and stores it in AWS PostgreSQL. Additionally, it integrates web scraping and NLP BERT sentiment analysis to quantify public sentiments, enriching stakeholders' comprehension of market dynamics.

![Crypto Project Flow](https://github.com/lunaSnowflake/CryptoCurrency/assets/110465395/9093e245-8b81-4b3e-81ac-540588969cba)

1. Data Collection
   - Use the "Coindesk" source to collect cryptocurrency price data.
   - Utilize the "Price Requester (Mage.ai-Python)" to fetch the prices from Coindesk.
   - Store the collected data in the "AWS S3" bucket.

2. Data Processing
   - Set up a "Kafka Server (AWS EC2)" to handle data streaming.
   - Create a "Producer" to send the collected price data to the Kafka server.
   - Implement a "Consumer" to receive the data from the Kafka server.

3. Data Storage and Analysis
   - Store the collected prices in the "AWS DB (Prices)" for further analysis.
   - Use the "AWS Crawler" to extract relevant information from the collected data.
   - Set up a "Forecast (Python)" module to predict future cryptocurrency prices.
   - Visualize the forecasted data using "PowerBI".
   - Store the forecasted prices in the "AWS DB (Forecasted)".

4. News Scrapping and Sentiment Analysis
   - Implement a "News Scrapping (Mage.ai-Python)" module to gather news articles related to cryptocurrencies from "Bing News" and "Coin MarketCap".
   - Perform sentiment analysis using "Sentiment Analysis (Hugging-Face)".
   - Store the sentiment analysis results in the "AWS DB (Sentiments)".

5. Project Integration
   - Combine all the collected and analyzed data to create a comprehensive view of the cryptocurrency market.
   - Use "PQ - Power Query" to clean and transform the data for further analysis or visualization.

## Features
- Real-time Data Capture: Utilizes an API to fetch real-time OHLC data for cryptocurrencies.
- Storage in AWS PostgreSQL: Stores the collected data securely in AWS PostgreSQL for further analysis.
- Sentiment Analysis: Integrates web scraping and NLP BERT sentiment analysis to quantify public sentiments related to cryptocurrencies.
- Machine Learning Forecasting: Develops and trains a machine learning forecasting model, updated daily through MageAI, offering accurate cryptocurrency forecasts.
- Dynamic Reporting with PowerBI: Engineers seamless data flow from PostgreSQL to PowerBI, creating a dynamic report showcasing market scenarios, trends, sentiments, and forecasts.
- Advanced Analysis Capabilities: Implements sophisticated DAX measures in PowerBI, equipping stakeholders with advanced statistical and technical analysis capabilities for informed decision-making in the volatile cryptocurrency landscape.
<br/>

![Power BI 1](https://github.com/lunaSnowflake/CryptoCurrency/assets/110465395/80c28dc0-daae-4e3c-9e15-06e8013c7db6)
![Power BI 2](https://github.com/lunaSnowflake/CryptoCurrency/assets/110465395/662ff6b6-2338-4b0e-9883-c199227ea669)

<br/>

## How to Use
- Clone the repository to your local machine.
- Set up AWS infrastructure with PostgreSQL.
- Configure MageAI for data orchestration.
- Run the provided scripts for data collection, sentiment analysis, and machine learning forecasting.
- Integrate the generated data with PowerBI for dynamic reporting.
- Explore the dashboard and leverage advanced analysis capabilities for insightful decision-making.
- Read [Doc.txt](https://github.com/lunaSnowflake/CryptoCurrency/blob/main/Doc.txt)

```
cd crypto_prices-Mage.ai
mage start
```

![Mage ai](https://github.com/lunaSnowflake/CryptoCurrency/assets/110465395/02354665-b405-404d-924c-542ffc31f7f9)

<!--[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/lunaSnowflake/CryptoCurrency)-->

<div align="center">
  <a href="https://gitpod.io/#https://github.com/lunaSnowflake/CryptoCurrency">
    <img src="https://gitpod.io/button/open-in-gitpod.svg" alt="Open in Gitpod">
  </a>
</div>



## 💻 Tech Stack
<img src="https://user-images.githubusercontent.com/25181517/183896128-ec99105a-ec1a-4d85-b08b-1aa1620b2046.png" width="50"> <!--SQL-->
<img width="48" height="48" src="https://img.icons8.com/color/48/power-bi-2021.png" alt="power-bi-2021"/> <!--PowerBI-->
<img src="https://user-images.githubusercontent.com/25181517/183896132-54262f2e-6d98-41e3-8888-e40ab5a17326.png" width="50"> <!--AWS-->
<img src="https://i.ibb.co/SXHDrpp/download.jpg" width="50"> <!--Mage.ai-->
<img src="https://user-images.githubusercontent.com/25181517/192107004-2d2fff80-d207-4916-8a3e-130fee5ee495.png" width="50"> <!--kafka-->
<img src="https://user-images.githubusercontent.com/25181517/184103699-d1b83c07-2d83-4d99-9a1e-83bd89e08117.png" width="50"> <!--Selenium-->
<img src="https://i.ibb.co/Cv2cdtM/33643075.png" width="50"> <!--Airflow-->
<img width="48" height="48" src="https://img.icons8.com/emoji/48/hugging-face.png" alt="hugging-face"/> <!--HuggingFace-->

### Languages
<img src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" width="50"> <!--Python-->

### Frameworks & Libraries (ML)
<img width="48" height="48" src="https://img.icons8.com/fluency/48/pytorch.png" alt="pytorch"/> <!--Pytorch-->
<img src="https://user-images.githubusercontent.com/25181517/223639822-2a01e63a-a7f9-4a39-8930-61431541bc06.png" width="50"> <!--Tensorflow-->
<img src="https://i.ibb.co/6ZqGyGR/OIP.jpg" width="50"> <!--Scikit Learn-->
<img width="48" height="48" src="https://img.icons8.com/material-rounded/24/keras.png" alt="keras"/>
<img width="48" height="48" src="https://img.icons8.com/color/48/numpy.png" alt="numpy"/>
<img width="48" height="48" src="https://img.icons8.com/color/48/pandas.png" alt="pandas"/>

### Others
<img src="https://user-images.githubusercontent.com/25181517/186884153-99edc188-e4aa-4c84-91b0-e2df260ebc33.png" width="50"> <!--Linux-->

## <img width="48" height="48" src="https://img.icons8.com/pulsar-color/48/about-me-male.png" alt="about-me-male"/> About Me

<font color="orange">Imagine a curious soul frolicking in the realm of Data Science and Development – that's me! With a heart brimming with joy, I dance through projects ranging from coding escapades to the magic of AI and DevOps. Technology isn't just my playground; it's my vibrant canvas where every line of code is a brushstroke of pure delight! <br/> I am open to any suggestions, connect with me anywhere! Also, I would appreciate it if I could get a 🌟</font> 
<br/>

![Dev Gif](https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif) <br/>

## 🌐 Socials
[![Github](https://img.icons8.com/ios-filled/50/github.png)](https://github.com/lunaSnowflake)
[![linkedin](https://img.icons8.com/fluency/48/linkedin.png)](https://www.linkedin.com/in/hussainkhatumdi/)
[<img src="https://i.ibb.co/5MsxX1w/kaggle-icon-512x512-ubnqei0x.png" width="48px">](https://www.kaggle.com/lunaticsain)
[![Medium](https://img.icons8.com/sf-regular-filled/48/medium-logo.png)](https://medium.com/@hussainkhatumadi53) 
[![Twitter](https://img.icons8.com/color/48/twitter--v1.png)](https://twitter.com/lunatic_sain) 
<br/>
<br/>

