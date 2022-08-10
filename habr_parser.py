from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def parse_habr_article(url):
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('headless')
    driver = Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.get(url)

    article_title = driver.find_element(
        By.CSS_SELECTOR,
        'h1.tm-article-snippet__title_h1'
    ).text

    article = driver.find_element(
        By.CSS_SELECTOR,
        'div.article-formatted-body'
    ).text

    print(article)
    print(article_title)


if __name__ == '__main__':
    url = 'https://habr.com/ru/company/pvs-studio/blog/681824/'
    parse_habr_article(url)
