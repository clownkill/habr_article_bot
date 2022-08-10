from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import gtts


def get_article_filename(article_title):
    return article_title.replace(": ", " ")


def save_article(article_title, article_body):
    article = f"{article_title}\n{article_body}"
    file_name = get_article_filename(article_title)
    text_file_name = file_name + ".txt"
    audio_file_name = file_name + ".mp3"

    with open(text_file_name, "w", encoding="utf-8") as f:
        f.write(article)

    gtts.gTTS(text=article_body, lang="ru").save(audio_file_name)

def parse_habr_article(url):
    options = ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("headless")
    driver = Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
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


if __name__ == "__main__":
    url = "https://habr.com/ru/post/681798/"
    article_title, article_body = parse_habr_article(url)
    save_article(article_title, article_body)
