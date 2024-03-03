if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
from bs4 import BeautifulSoup

@custom
def transform_custom(*args, **kwargs):
    print('1')
    query = "US+cryptocurrency+market+news"
    url = f"https://www.bing.com/news/search?q={query}&qft=interval%3d\"7\"&form=PTFTNR"

    print('2')
    firefox_options = Options()
    firefox_options.add_argument("--no-sandbox") # Disabling the sandboxing process for the browser
    firefox_options.add_argument("--headless")
    print('2.1')
    driver = webdriver.Firefox(options=firefox_options)
    driver.set_page_load_timeout(5)

    print('3')
    driver.get(url)

    print('4')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.delete_all_cookies()
    driver.quit()

    print('5')
    all_news_container = soup.find_all(class_="news-card newsitem cardcommon")

    news_urls = []

    pattern = r"(?<=\surl\=\").+(?=\"><div class=\"news-card-body card-with-cluster)"
    for news_card in tqdm(all_news_container, total=len(all_news_container)):
        news_urls.append(re.findall(pattern, str(news_card))[0])

    print(f"All {len(all_news_container)} urls extracted successfully!"
            if len(all_news_container)==len(news_urls)
            else f"Only {len(news_urls)} urls could be extracted!")

    return "hi"


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
