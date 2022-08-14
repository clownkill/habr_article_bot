from environs import Env
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import gtts


env = Env()
env.read_env()


def get_web_driver():
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    return Chrome(
        executable_path=env('CHROME_DRIVER_PATH'),
        options=options
    )


def get_article_filename(article_title):
    return article_title.replace(": ", " ") + ".mp3"


def save_article(article_title, article_body):
    article = f"{article_title}\n{article_body}"
    file_name = get_article_filename(article_title)

    gtts.gTTS(text=article, lang="ru").save(file_name)


def parse_habr_article(url):
    driver = get_web_driver()
    driver.get(url)

    article_title = driver.find_element(
        By.CSS_SELECTOR,
        "h1.tm-article-snippet__title_h1"
    ).text

    article_body = driver.find_element(
        By.CSS_SELECTOR,
        "div.article-formatted-body"
    ).text

    return article_title, article_body


def get_last_articles(url):
    driver = get_web_driver()
    driver.get(url)

    articles = driver.find_elements(
        By.CSS_SELECTOR,
        "a.tm-article-snippet__title-link"
    )

    last_articles = {
        article.text: article.get_attribute("href") for article in articles
    }

    return last_articles


if __name__ == "__main__":
    url = "https://habr.com/ru/all/"
    get_last_articles(url)
