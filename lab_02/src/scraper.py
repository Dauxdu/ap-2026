from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def fetch(url: str) -> requests.Response:
    """
    Выполняет GET-запрос и проверяет статус ответа.

    :param url: адрес для запроса
    :return: ответ сервера
    :raises requests.RequestException: при ошибке сети или статусе 4xx/5xx
    """
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response


def get_soup(url: str) -> BeautifulSoup:
    """
    Загружает страницу и разбирает её HTML.

    :param url: адрес страницы
    :return: дерево разобранной страницы
    """
    return BeautifulSoup(fetch(url).content, "html.parser")


def get_genres() -> dict[str, str]:
    """
    Получает жанры из боковой панели главной страницы.

    :return: словарь {название жанра: адрес страницы жанра}
    """
    links = get_soup(BASE_URL).select("div.side_categories ul ul a")
    return {
        link.get_text(strip=True): urljoin(BASE_URL, link["href"]) for link in links
    }


def get_book_urls(genre_url: str, count: int) -> list[str]:
    """
    Собирает адреса страниц книг жанра, переходя по страницам списка.

    :param genre_url: адрес первой страницы жанра
    :param count: сколько книг нужно
    :return: не более count адресов страниц книг
    """
    book_urls = []
    page_url = genre_url
    while page_url and len(book_urls) < count:
        soup = get_soup(page_url)
        for link in soup.select("article.product_pod h3 a"):
            book_urls.append(urljoin(page_url, link["href"]))
        next_link = soup.select_one("li.next a")
        page_url = urljoin(page_url, next_link["href"]) if next_link else None
    return book_urls[:count]


def get_cover_url(book_url: str) -> str:
    """
    Получает адрес полноразмерной обложки со страницы книги.

    :param book_url: адрес страницы книги
    :return: адрес обложки
    """
    image = get_soup(book_url).select_one("#product_gallery img")
    return urljoin(book_url, image["src"])


def download_file(url: str, file_path: str) -> None:
    """
    Скачивает файл и сохраняет его на диск.

    :param url: адрес файла
    :param file_path: путь для сохранения
    """
    content = fetch(url).content
    with open(file_path, "wb") as file:
        file.write(content)
